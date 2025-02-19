from constants import MAIN_WINDOW_BG_COLOR
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from state_manager import StateManager, AppState
from lightroom import LightroomAutomationThread
from lightroom.LightroomLaunchThread import LightroomLaunchThread
from helpers.log_exception_to_file import log_exception_to_file
from ui.msg_box import create_error_msg
from ui.inputs.input_main_field import input_main_field
from ui.buttons.btn_run_main import btn_run_main
from ui.msg_box.show_guide import show_guide
from ui.overlay.OverlayWindow import OverlayWindow


class MainWindow(QMainWindow):
    def __init__(
        self,
        width=300,
        height=200,
        lock_user_input=True,
    ):
        super().__init__()

        self.lock_user_input = lock_user_input

        self.init_state_manager()
        self.setWindowTitle("다비 내보내기 매니저")

        self.setWindowIcon(QIcon("assets/다비스튜디오_logo11_black_ico.ico"))

        self.setObjectName("MainWindow")
        self.setStyleSheet(
            f"""
            #MainWindow {{
                background-color: {MAIN_WINDOW_BG_COLOR};
            }}
            """
        )

        self.init_window_position(
            height=height,
            width=width,
        )
        self.init_window_layout()

        self.overlay_window = None
        self.thread_lightroom_automation = None
        self.thread_lightroom_launcher = None

    def init_input_main_fields(self, layout):
        self.input_username = input_main_field(
            layout=layout,
            label="예약자 성함",
            placeholder="“여기에 입력하세요.”",
        )
        self.input_phone = input_main_field(
            layout=layout,
            label="전화번호 뒷자리 4자리",
            placeholder="“여기에 입력하세요.”",
        )

    def init_window_layout(self):
        layout = QVBoxLayout()

        self.init_input_main_fields(layout=layout)

        self.run_button = btn_run_main()
        self.run_button.clicked.connect(self.run_main_window)

        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_state_manager(self):
        self.state_manager = StateManager()
        self.state_manager.subscribe(self.on_state_global_change)  # 상태 변경 구독

    def init_window_position(self, width, height):
        """창을 화면 정중앙 (상하 & 좌우) 정렬"""

        #  현재 화면의 해상도 가져오기
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        x = (screen_width - width) // 2  # 좌우 정가운데
        y = (screen_height - height) // 2  # 상하 정가운데

        # 창의 위치 및 크기 설정
        self.setGeometry(x, y, width, height)

        # 창을 항상 최상단에 고정
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def init_threads(self):
        # 라이트룸 실행 스레드
        self.thread_lightroom_launcher = LightroomLaunchThread()
        self.thread_lightroom_launcher.lightroom_started.connect(
            self.on_lightroom_launcher
        )

        # 자동화 스레드
        self.thread_lightroom_automation = LightroomAutomationThread(
            lock_user_input=self.lock_user_input
        )
        self.thread_lightroom_automation.finished.connect(
            self.on_lightroom_automation_finished
        )
        self.thread_lightroom_automation.failed.connect(
            self.on_lightroom_automation_failed
        )

    def on_overlay_closed(self):
        """✅ 오버레이가 닫힐 때 호출되는 부모 이벤트 핸들러"""
        print("✅ 부모 윈도우에서 오버레이 닫힘 감지 완료!")
        self.overlay_window = None  # ✅ 메모리 해제

    def close_overlay(self):
        if self.overlay_window:
            self.overlay_window.close()
            self.overlay_window.deleteLater()
            self.overlay_window = None

    def run_main_window(self):
        self.init_threads()

        try:
            username = self.input_username.text().strip()
            phone_number = self.input_phone.text().strip()

            if username == "":
                QMessageBox.warning(self, "입력 오류", "사용자 이름을 입력하세요!")
                return

            if phone_number == "":
                QMessageBox.warning(
                    self, "입력 오류", "전화번호 뒷자리 4자리를 입력하세요!"
                )
                return

            self.showMinimized()

            self.state_manager.update_state(
                phone_number=phone_number,
                username=username,
                context="사용자정보 올바르게 입력함",
            )

            self.thread_lightroom_launcher.start()

        except Exception as e:
            self.show_err_msg()
            log_exception_to_file(
                exception_obj=e, message="메인 프로그램 실행 중 예외발생"
            )

    def show_err_msg(self):
        error_msg_box = create_error_msg(parent=self)
        error_msg_box.exec()

    def create_overlay(self):
        """독립적인 오버레이 창을 생성하고 부모 윈도우와 시그널 연결"""
        if self.overlay_window is not None:
            print("이미 오버레이가 생성 중입니다.")
            return

        self.overlay_window = OverlayWindow()  #  독립적인 오버레이 생성
        self.overlay_window.show()

    def on_lightroom_launcher(self, lightroom_started):
        if lightroom_started == True:
            print("Main - 라이트룸 활성화 완료")

            self.create_overlay()
            print("Main - 오버레이 실행 시작")

            self.thread_lightroom_automation.start()
            print("Main - 라이트룸 자동화 시작")

    def on_lightroom_automation_finished(self, finished):
        if self.overlay_window is not None and finished == True:
            self.close_overlay()

            if show_guide(self):
                self.cleanup_resources()
                self.close()  # 메인 윈도우 종료 요청

    def on_lightroom_automation_failed(self, failed_automation):
        if failed_automation == False:
            return
        self.close_overlay()
        self.show()
        self.show_err_msg()

        self.cleanup_resources()

        self.close()  # 메인 윈도우 종료 요청

    def on_state_global_change(self, new_state: AppState):
        print(
            f"----------------- [📢] 상태 변경 감지: {new_state.context} -----------------"
        )
        print(f"사용자이름: {new_state.username}")
        print(f"전화번호: {new_state.phone_number}")

    def show_warning(self, text="⚠️ 경고: 잘못된 작업입니다."):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)  # ⚠️ 경고 아이콘
        msg_box.setWindowTitle("경고")  # 창 제목
        msg_box.setText(text)  # 메시지 내용
        msg_box.setStandardButtons(QMessageBox.Ok)  # 확인 버튼 추가
        msg_box.exec()  # 메시지 박스 실행

    def closeEvent(self, event):
        """메인 윈도우가 닫힐 때 모든 리소스 정리"""
        print(" 프로그램 종료: 모든 리소스 정리 중...")

        self.cleanup_resources()

        print(" 모든 리소스 정리 완료. 프로그램 종료.")
        event.accept()  #  정상적으로 창을 닫음

    def cleanup_resources(self):
        """실행 중인 스레드와 오버레이 창을 안전하게 종료 및 정리"""
        if self.thread_lightroom_automation:
            print(" Lightroom 자동화 스레드 종료 중...")

            # ✅ 스레드 종료 요청
            self.thread_lightroom_automation.quit()

            # ✅ Qt가 자동으로 정리할 수 있도록 deleteLater() 호출
            self.thread_lightroom_automation.deleteLater()
            self.thread_lightroom_automation = None

        if self.overlay_window:
            print(" 오버레이 창 닫기...")
            self.overlay_window.close()
            self.overlay_window.deleteLater()
            self.overlay_window = None
