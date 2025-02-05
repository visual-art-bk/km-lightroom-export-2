import time
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
from monitorings.LightroomMonitorThread import LightroomMonitorThread


class MainWindow(QMainWindow):
    """Lightroom 실행 GUI"""

    def __init__(self, x=None, y=0, width=300, height=200):
        super().__init__()

        self.init_state_manager()

        self.setWindowTitle("라이트룸 촬영 매니저")

        self.init_window_position(
            height=height, x=x, screen_width=self.get_screen_width(), width=width, y=y
        )

        self.init_window_layout()

        self.overlay_window = None
        self.lightroom_monitor = None
        self.thread_lightroom_automation = None

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

        self.run_button = QPushButton("Lightroom 실행")
        self.run_button.clicked.connect(self.run_main_window)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_state_manager(self):
        self.state_manager = StateManager()
        self.state_manager.subscribe(self.ON_STATE_CHANGE)  # 상태 변경 구독

    def init_window_position(self, x, y, width, height, screen_width):
        # 항상 최상단에 고정
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # ✅ 사용자가 x를 설정하지 않으면 기본값으로 "우측 상단" 위치 지정
        if x is None:
            x = screen_width - width  # 우측 끝으로 정렬

        # ✅ 창의 초기 위치 및 크기 설정 (기본값: 화면 우측 상단)
        self.setGeometry(x, y, width, height)

    def get_screen_width(self):
        # 현재 화면 크기 가져오기
        screen = QApplication.primaryScreen().availableGeometry()
        return screen.width()  # 화면 전체 너비

    def delete_overlay(self):
        self.overlay_window = None
        OverlayWindow._instance = None

    def get_user_infos(self):
        return {
            "username": self.username_entry.text().strip(),
            "phone_number": self.phone_number_entry.text().strip(),
        }

    def init_threads(self):
        self.thread_lightroom_automation = LightroomAutomationThread()
        self.thread_lightroom_mornitor = LightroomMonitorThread()

        self.thread_lightroom_automation.is_run_lightroom.connect(
            self.on_lightroom_automation_is_run_lightroom
        )
        self.thread_lightroom_automation.finished.connect(
            self.on_lightroom_automation_finished
        )
        self.thread_lightroom_mornitor.lightroom_closed_mornitoring.connect(
            self.on_lightroom_closed_mornitoring
        )

    def run_main_window(self):
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

        self.state_manager.update_state(
            phone_number=phone_number,
            username=username,
            context="사용자정보 올바르게 입력함",
        )

        self.init_threads()

        self.thread_lightroom_automation.start()

    def create_overlay(self, text="마우스 및 키보드를 절대 건들지 마세요 :)"):
        """✅ `overlay_running=True`이면 OverlayWindow 생성"""
        if self.overlay_window is None:
            self.overlay_window = OverlayWindow.create_overlay(
                width=1200,
                height=250,
                bg_color="#ff0000",
                opacity=0.3,
                text=text,
                text_color="black",
                font_size=48,
                animation_speed=25,
                y_offset=50,
                blur_radius=50,
            )
            self.overlay_window.show()
        else:
            print("해당없음")

    def show_warning(self, text="⚠️ 경고: 잘못된 작업입니다."):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)  # ⚠️ 경고 아이콘
        msg_box.setWindowTitle("경고")  # 창 제목
        msg_box.setText(text)  # 메시지 내용
        msg_box.setStandardButtons(QMessageBox.Ok)  # 확인 버튼 추가
        msg_box.exec()  # 메시지 박스 실행

    def on_lightroom_automation_is_run_lightroom(self, is_run_lightroom):
        if is_run_lightroom == False:
            self.state_manager.update_state(
                context="라이트룸이 먼저 실행되지 않았음", lightroom_running=False
            )
            self.show_warning("⚠️ 경고: 라이트 룸을 먼저 실행하세요.")
            return

        time.sleep(2)

        self.create_overlay(
            text="내보내기 셋팅중이에요, 마우스 및 키보드를 절대 건들지 마세요 :)"
        )

        self.state_manager.update_state(
            context="오버레이 실행 완료",
            overlay_running=True,
        )

        self.thread_lightroom_mornitor.start()

    def on_lightroom_automation_finished(self, finished):
        if finished == False:
            return
        # ✅ 메시지 박스 생성
        msg_box = QMessageBox(
            self
        )  # ✅ 부모 윈도우 설정 (현재 윈도우가 닫혀도 메시지박스 유지)
        msg_box.setIcon(QMessageBox.Icon.Information)  # ℹ️ 정보 아이콘 설정
        msg_box.setWindowTitle("알림")  # 창 제목
        msg_box.setText(
            "📸 내보내기가 시작됐어요!\n\n"
            "⏳ 약 10분 정도 소요됩니다.\n\n"
            "✅ '확인' 버튼을 눌러주시고,\n"
            "🎨 촬영 소품, 배경지, 리모컨을 정리한 후\n"
            "🚶‍♂️ 셀렉실로 이동해주세요."
        )  # 메시지 내용

        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)  # "확인" 버튼 추가

        # ✅ 메시지 박스를 항상 최상위 창으로 설정
        msg_box.setWindowFlags(
            Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
        )

        # ✅ 메시지 박스를 먼저 띄운 후 크기 확정
        msg_box.adjustSize()  # 크기를 자동으로 조정
        msg_box.show()  # 크기를 확정하기 위해 먼저 표시
        msg_box.repaint()  # UI 갱신 (위치 보정)

        # ✅ 화면 정중앙에 메시지 박스를 배치
        if self.isVisible():  # 메인 윈도우가 존재하면
            parent_geometry = self.frameGeometry()
            msg_box_geometry = msg_box.frameGeometry()
            msg_box_geometry.moveCenter(
                parent_geometry.center()
            )  # 메인 윈도우 중앙 좌표로 이동
            msg_box.move(msg_box_geometry.topLeft())  # 최종 이동
        else:  # 메인 윈도우가 보이지 않는다면, 화면 정중앙에 배치
            screen_geometry = msg_box.screen().availableGeometry()
            msg_box_geometry = msg_box.frameGeometry()
            msg_box_geometry.moveCenter(screen_geometry.center())  # 전체 화면 중앙 좌표
            msg_box.move(msg_box_geometry.topLeft())

        # ✅ 메시지 박스를 띄우고 사용자가 버튼을 클릭할 때까지 대기
        msg_box.exec()

        # ✅ "확인" 버튼 클릭 후 메인 윈도우 숨기기
        if self.overlay_window is not None:
            self.delete_overlay()

        self.state_manager.update_state(
            context="자동화 끝! 오버레이 종료",
            overlay_running=False,
        )

        self.hide()

    def on_lightroom_closed_mornitoring(self):
        print("✅ Lightroom 종료 감지 → 프로그램 종료")

        self.state_manager.update_state(
            context="Lightroom 종료 → 프로그램 종료",
            lightroom_running=False,
        )

        QApplication.quit()  # ✅ `QApplication` 종료 (완전히 종료)

    def ON_STATE_CHANGE(self, new_state: AppState):
        """전역 상태 변경 감지 및 UI 반영"""
        print(
            f"----------------- [📢] 상태 변경 감지: {new_state.context} -----------------"
        )
        print(f"사용자이름: {new_state.username}")
        print(f"전화번호: {new_state.phone_number}")
        print(f"라이트룸 실행여부: {'실행' if new_state.lightroom_running else '중지'}")
        print(f"오버레이 실행여부: {'실행' if new_state.overlay_running else '중지'}")
        print(f"                                                      ")
