import time
import psutil
from pywinauto import Application
from .utils.get_lightroom_win import get_lightroom_win
from lightroom.exports.run_exports import run_exports
from PySide6.QtCore import QThread, Signal
from helpers import log_exception_to_file

class LightroomAutomationThread(QThread):
    """Lightroom 자동화 실행을 위한 스레드"""

    failed_automation = Signal(bool)

    finished = Signal(bool)  # ✅ 성공/실패 여부를 전달하는 시그널

    def __init__(self, lock_user_input):
        super().__init__()
        self.lock_user_input = lock_user_input

    def run(self):
        """Lightroom 자동화를 실행하는 메인 스레드"""

        # ✅ 1️⃣ Lightroom 실행 여부 확인
        lightroom_pid = None
        for process in psutil.process_iter(attrs=["name", "pid", "exe"]):
            if "Lightroom.exe" in process.info["name"]:
                lightroom_pid = process.info["pid"]
                break  # 첫 번째 Lightroom 프로세스 사용

        if not lightroom_pid:
            print("❌ Lightroom이 실행 중이 아닙니다. 먼저 실행해주세요.")
            return

        print(f"✅ Lightroom 실행 감지됨 (PID: {lightroom_pid})")

        # ✅ 2️⃣ Lightroom 프로세스에 직접 연결
        try:
            app = Application(backend="uia").connect(process=lightroom_pid, timeout=15)
            print("✅ Lightroom에 성공적으로 연결됨!")

            # ✅ 3️⃣ Lightroom 창 활성화 확인 및 복구
            lightroom = get_lightroom_win(app)
            
        except Exception as e:
            print(f"❌ Lightroom 연결 실패: {e}")
            log_exception_to_file(exception_obj=e, message='Lightroom 연결 실패')
            self.failed_automation.emit(True)  # ❌ 연결 실패 시그널 발생
            return

        try:
            # ✅ 5️⃣ Lightroom 내보내기 자동화 실행
            print("🚀 Lightroom 내보내기 자동화 실행 중...")
            run_exports(lightroom=lightroom, lock_user_input=self.lock_user_input)

            print("✅ Lightroom 자동화 완료 🚀")
            self.finished.emit(True)  # ✅ 자동화 성공 시그널 발생

        except Exception as e:
            print(f"❌ Lightroom 자동화 실패: {e}")
            log_exception_to_file(exception_obj=e, message='Lightroom 자동화 실패')
            self.failed_automation.emit(True)  # ❌ 연결 실패 시그널 발생
