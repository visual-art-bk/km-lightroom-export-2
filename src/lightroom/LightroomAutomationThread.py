import ctypes
import pyautogui
import time
from pywinauto import Application, keyboard
from lightroom.exports.run_exports import run_exports
from PySide6.QtCore import QThread, Signal
from helpers import log_exception_to_file
from mornitorings.TaskManagerDetector import TaskManagerDetector


def lock_input():
    """✅ 마우스와 키보드 입력을 잠급니다 (Windows 전용)"""
    ctypes.windll.user32.BlockInput(True)  # 🔒 입력 차단
    pyautogui.FAILSAFE = False  # ⛔ 마우스 모서리 이동 방지


def unlock_input():
    """✅ 마우스와 키보드 입력을 다시 활성화합니다"""
    ctypes.windll.user32.BlockInput(False)  # 🔓 입력 해제


class LightroomAutomationThread(QThread):
    failed = Signal(bool)
    finished = Signal(bool)

    def __init__(self, lock_user_input):
        super().__init__()
        self.lock_user_input = lock_user_input
        self.stop_flag = False  # ✅ 자동화 중지 플래그
        self.task_detector = TaskManagerDetector(self.stop_automation)

    def stop_automation(self):
        """✅ `Ctrl + Alt + Delete` 감지 시 자동화 강제 중단"""
        print("❌ 자동화 강제 중단됨!")
        self.stop_flag = True
        unlock_input()  # ✅ 입력 차단 해제
        self.task_detector.stop()  # ✅ 키 감지 스레드 종료
        self.finished.emit(False)  # ❌ 자동화 실패 시그널 발생
        self.quit()

    def run(self):
        try:
            if self.lock_user_input == True:
                lock_input()

            self.task_detector.start()
            if self.stop_flag:
                return

            app = Application(backend="uia").connect(
                title_re=".*Lightroom Classic.*", timeout=15
            )

            lightroom = app.window(title_re=".*Lightroom Classic.*")

            lightroom.wait("exists enabled visible ready", timeout=10)

            print("Lightroom에 성공적으로 연결됨!")

            lightroom.wrapper_object().maximize()
            lightroom.wrapper_object().set_focus()

            run_exports(lightroom=lightroom)

            print("Lightroom 자동화 완료")
            self.finished.emit(True)

        except Exception as e:
            print(f"Lightroom 자동화 실패: {e}")
            log_exception_to_file(exception_obj=e, message="Lightroom 자동화 실패")
            self.failed.emit(True)

        finally:
            if self.lock_user_input == True:
                lock_input()
