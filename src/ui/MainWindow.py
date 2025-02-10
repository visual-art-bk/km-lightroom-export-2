import os
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QApplication,
)
from PySide6.QtCore import Qt
from state_manager import StateManager, AppState
from lightroom import LightroomAutomationThread
from ui.overlay.OverlayWindow import OverlayWindow
from ui.msg_box import create_error_msg, create_done_msg
from monitorings.LightroomMonitorThread import LightroomMonitorThread
from lightroom.LightroomLaunchThread import LightroomLaunchThread


class MainWindow(QMainWindow):
    def __init__(
        self,
        x=None,
        y=0,
        width=300,
        height=200,
        lock_user_input=True,
        overlay_mode=True,
    ):
        super().__init__()

        self.lock_user_input = lock_user_input

        self.overlay_mode = overlay_mode

        self.init_state_manager()

        self.setWindowTitle("다비 내보내기 베타 V.1.0")

        self.init_window_position(
            height=height,
            width=width,
        )

        self.init_window_layout()

        self.overlay_window = None
        self.lightroom_monitor = None
        self.thread_lightroom_automation = None
        self.thread_lightroom_mornitor = None
        self.thread_lightroom_launcher = None

    def init_window_layout(self):
        layout = QVBoxLayout()

        self.label_username = QLabel("예약자 이름")
        layout.addWidget(self.label_username)

        self.username_entry = QLineEdit()
        layout.addWidget(self.username_entry)

        self.label_phone_number = QLabel("전화번호 뒷자리 4자리")
        layout.addWidget(self.label_phone_number)

        self.phone_number_entry = QLineEdit()
        layout.addWidget(self.phone_number_entry)

        self.run_button = QPushButton("📁 내보내기 시작")
        self.run_button.clicked.connect(self.run_main_window)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_state_manager(self):
        self.state_manager = StateManager()
        self.state_manager.subscribe(self.on_state_global_change)  # 상태 변경 구독

    def init_window_position(self, width, height):
        """✅ 창을 화면 정중앙 (상하 & 좌우) 정렬"""

        # ✅ 현재 화면의 해상도 가져오기
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # ✅ 창을 화면 정중앙에 배치 (좌우 & 상하)
        x = (screen_width - width) // 2  # 좌우 정가운데
        y = (screen_height - height) // 2  # 상하 정가운데

        # ✅ 창의 위치 및 크기 설정
        self.setGeometry(x, y, width, height)

        # ✅ 창을 항상 최상단에 고정
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def delete_overlay(self):
        self.overlay_window = None
        OverlayWindow._instance = None

    def get_user_infos(self):
        return {
            "username": self.username_entry.text().strip(),
            "phone_number": self.phone_number_entry.text().strip(),
        }

    def init_threads(self):
        self.thread_lightroom_launcher = LightroomLaunchThread()

        self.thread_lightroom_automation = LightroomAutomationThread(
            lock_user_input=self.lock_user_input
        )
        self.thread_lightroom_mornitor = LightroomMonitorThread()

        self.thread_lightroom_launcher.lightroom_started.connect(
            self.on_lightroom_launcher
        )
        self.thread_lightroom_automation.finished.connect(
            self.on_lightroom_automation_finished
        )
        self.thread_lightroom_mornitor.lightroom_closed_mornitoring.connect(
            self.on_lightroom_closed_mornitoring
        )
        self.thread_lightroom_automation.failed_automation.connect(
            self.on_lightroom_automation_failed
        )

    def run_main_window(self):
        try:
            userer_infos = self.get_user_infos()
            username = userer_infos["username"]
            phone_number = userer_infos["phone_number"]

            if username == "":
                QMessageBox.warning(self, "입력 오류", "사용자 이름을 입력하세요!")
                return

            if phone_number == "":
                QMessageBox.warning(
                    self, "입력 오류", "전화번호 뒷자리 4자리를 입력하세요!"
                )
                return

            self.hide()

            self.state_manager.update_state(
                phone_number=phone_number,
                username=username,
                context="사용자정보 올바르게 입력함",
            )

            self.init_threads()

            self.thread_lightroom_launcher.start()

        except:
            self.show_err_msg()

    def on_lightroom_automation_failed(self, failed_automation):
        if failed_automation == False:
            return

        self.delete_overlay()
        self.state_manager.update_state(
            context="자동화 에러 발생! 오버레이 종료",
            overlay_running=False,
        )

        self.show()
        self.show_err_msg()

    def on_lightroom_launcher(self, lightroom_started):
        if lightroom_started == False:
            self.state_manager.update_state(
                context="라이트룸이 먼저 실행되지 않았음", lightroom_running=False
            )
            self.show_warning("⚠️ 경고: 라이트 룸을 먼저 실행하세요.")
            return

        self.thread_lightroom_mornitor.start()

        if self.overlay_mode == True:
            self.create_overlay()

        self.state_manager.update_state(
            context="오버레이 실행 완료",
            overlay_running=True,
        )

        self.thread_lightroom_automation.start()

    def on_lightroom_automation_finished(self, finished):
        if self.overlay_window is not None and finished == True:
            self.delete_overlay()

            self.thread_lightroom_launcher.minimize_lightroom_window()

            self.state_manager.update_state(
                context="자동화 끝! 오버레이 종료",
                overlay_running=False,
            )

            self.show()

            msg_box = create_done_msg(parent=self)

            msg_box.exec()

            self.cleanup_and_exit()

    def on_lightroom_closed_mornitoring(self):
        print("✅ Lightroom 종료 감지 → 프로그램 종료")

        self.state_manager.update_state(
            context="Lightroom 종료 → 프로그램 종료",
            lightroom_running=False,
        )

        self.cleanup_and_exit()

    def on_state_global_change(self, new_state: AppState):
        """전역 상태 변경 감지 및 UI 반영"""
        print(
            f"----------------- [📢] 상태 변경 감지: {new_state.context} -----------------"
        )
        print(f"사용자이름: {new_state.username}")
        print(f"전화번호: {new_state.phone_number}")
        print(f"라이트룸 실행여부: {'실행' if new_state.lightroom_running else '중지'}")
        print(f"오버레이 실행여부: {'실행' if new_state.overlay_running else '중지'}")
        print(f"                                                      ")

    def cleanup_and_exit(self):
        """💡 프로그램 종료 전 모든 리소스를 완전히 정리하는 함수"""
        print("🔄 모든 리소스 정리 중...")

        # ✅ 1. 스레드 강제 종료 (QThread가 완전히 종료되었는지 확인)
        if self.thread_lightroom_automation:
            if self.thread_lightroom_automation.isRunning():
                print("⚠️ Lightroom 자동화 스레드 강제 종료")
                self.thread_lightroom_automation.terminate()
            self.thread_lightroom_automation.quit()
            self.thread_lightroom_automation.wait()
            self.thread_lightroom_automation = None

        if self.thread_lightroom_mornitor:
            if self.thread_lightroom_mornitor.isRunning():
                print("⚠️ Lightroom 모니터링 스레드 강제 종료")
                self.thread_lightroom_mornitor.terminate()
            self.thread_lightroom_mornitor.quit()
            self.thread_lightroom_mornitor.wait()
            self.thread_lightroom_mornitor = None

        # ✅ 2. 오버레이 정리 (UI 리소스 해제)
        if self.overlay_window:
            self.overlay_window.close()
            self.overlay_window.deleteLater()
            self.overlay_window = None
        OverlayWindow._instance = None  # 싱글톤 인스턴스 초기화

        # ✅ 3. 상태 관리자 해제
        self.state_manager = None

        # ✅ 4. UI 창 닫기
        self.close()
        self.deleteLater()  # UI 객체를 명시적으로 제거

        # ✅ 5. QApplication 완전 종료
        QApplication.quit()

        # ✅ 6. **운영체제 프로세스 강제 종료 (최후의 수단)**
        print("🚀 모든 리소스 해제 완료 → 시스템 프로세스 강제 종료")
        os._exit(0)  # 💀 시스템 차원에서 프로세스 완전 제거

    def create_overlay(self):
        if self.overlay_window is not None:
            print("이미 오버레이가 생성중입니다.")
            return

        self.overlay_window = OverlayWindow.create_overlay(
            width=400,
            height=225,
            bg_color="#f7dfdf",
            opacity=1,
            text_color="black",
            font_size=20,
            y_offset=24,
            blur_radius=50,
        )
        self.overlay_window.show()

    def show_warning(self, text="⚠️ 경고: 잘못된 작업입니다."):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)  # ⚠️ 경고 아이콘
        msg_box.setWindowTitle("경고")  # 창 제목
        msg_box.setText(text)  # 메시지 내용
        msg_box.setStandardButtons(QMessageBox.Ok)  # 확인 버튼 추가
        msg_box.exec()  # 메시지 박스 실행

    def show_err_msg(self):
        error_msg_box = create_error_msg(parent=self)
        error_msg_box.exec()
