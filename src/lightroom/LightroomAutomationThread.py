from pywinauto import Application
from state_manager.StateManager import StateManager
from .utils.get_lightroom_win import get_lightroom_win
from PySide6.QtCore import QThread, Signal
from lightroom.exports.run_exports import run_exports

class LightroomAutomationThread(QThread):
    """Lightroom 자동화 실행을 위한 스레드"""

    finished = Signal(bool)  # ✅ 성공/실패 여부를 전달하는 시그널

    def __init__(self):
        super().__init__()

    def run(self):
        # ✅ Lightroom 프로세스에 직접 연결
        try:
            app = Application(backend="uia").connect(
                path=r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe",
                timeout=15,  # Lightroom 연결 시도 (최대 15초 대기)
            )
            print("✅ Lightroom에 성공적으로 연결됨!")
        except Exception as e:
            print(f"❌ Lightroom 연결 실패: {e}")
            self.finished.emit(False)  # ❌ 연결 실패 시그널 발생
            return

        # ✅ Lightroom 창 가져오기
        lightroom = get_lightroom_win(app)
        
        try:
            run_exports(lightroom=lightroom)
            
            print("✅ Lightroom 자동화 완료 🚀")
            self.finished.emit(True)  # ✅ 자동화 성공 시그널 발생

        except Exception as e:
            print(f"❌ Lightroom 자동화 실패: {e}")
            self.finished.emit(False)  # ❌ 자동화 실패 시그널 발생
