from pywinauto import Application
from lightroom.exports.run_exports import run_exports
from PySide6.QtCore import QThread, Signal
from helpers import log_exception_to_file


class LightroomAutomationThread(QThread):
    failed_automation = Signal(bool)

    finished = Signal(bool)

    def __init__(self, lock_user_input):
        super().__init__()
        self.lock_user_input = lock_user_input

    def run(self):
        try:
            app = Application(backend="uia").connect(
                title_re=".*Lightroom Classic.*", timeout=15
            )

            lightroom = app.window(title_re=".*Lightroom Classic.*")

            lightroom.wait("exists enabled visible ready", timeout=10)

            print("Lightroom에 성공적으로 연결됨!")

            lightroom.wrapper_object().maximize()

            run_exports(lightroom=lightroom, lock_user_input=self.lock_user_input)

            print("Lightroom 자동화 완료")
            self.finished.emit(True)

        except Exception as e:
            print(f"Lightroom 자동화 실패: {e}")
            log_exception_to_file(exception_obj=e, message="Lightroom 자동화 실패")
            self.failed_automation.emit(True)
