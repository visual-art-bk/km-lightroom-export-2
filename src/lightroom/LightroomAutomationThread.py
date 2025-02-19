import ctypes
import pyautogui
from pywinauto import Application
from lightroom.exports.run_exports import run_exports
from PySide6.QtCore import QThread, Signal
from helpers import log_exception_to_file
from mornitorings.TaskManagerDetector import TaskManagerDetector


def lock_mouse_keyboard():
    """✅ 마우스와 키보드 입력을 잠급니다 (Windows 전용)"""
    ctypes.windll.user32.BlockInput(True)  # 🔒 입력 차단
    pyautogui.FAILSAFE = False  # ⛔ 마우스 모서리 이동 방지


def unlock_mouse_keyboard():
    """✅ 마우스와 키보드 입력을 다시 활성화합니다"""
    ctypes.windll.user32.BlockInput(False)  # 🔓 입력 해제


class LightroomAutomationThread(QThread):
    failed = Signal(bool)
    finished = Signal(bool)

    def __init__(self, lock_user_input):
        super().__init__()
        self.lock_user_input = lock_user_input
        self.stop_flag_count = 0
        self.stop_flag = False  # ✅ 자동화 중지 플래그
        self.task_detector = TaskManagerDetector(self.stop_automation)

    def stop_automation(self):
        """✅ `Ctrl + Alt + Delete` 감지 시 자동화 강제 중단"""
        print("❌ 자동화 강제 중단됨!")

        self.stop_flag = True

        unlock_mouse_keyboard()

        self.finished.emit(False)  # ❌ 자동화 실패 시그널 발생

        log_exception_to_file(
            exception_obj=None, message="Ctrl + Alt + Delete 감지로 자동화 강제 중단"
        )

        self.quit()

    def check_stop_flag(self, context=''):
        if self.stop_flag_count == 1:
            print('작업관리자 실행으로 인한 자동화 중단 감지를 이미 실행했습니다.')
            self.stop_flag = True
            return self.stop_flag
        
        if self.stop_flag == True:
            print(f"⛔ 자동화 중단 감지! 실행 중지 {context}")
            self.failed.emit(True)
            self.stop_flag_count = 1
            return self.stop_flag
        

    def run(self):
        try:
            if self.lock_user_input == True:
                lock_mouse_keyboard()

            # task_detector는 독립적인 백그라운드 실행으로
            # 나중에 호출되는 run_exports에서도
            # 작업관리자 실행을 감지하고 있음.
            self.task_detector.start()
            self.check_stop_flag()

            app = Application(backend="uia").connect(
                title_re=".*Lightroom Classic.*", timeout=15
            )

            lightroom = app.window(title_re=".*Lightroom Classic.*")

            lightroom.wait("exists enabled visible ready", timeout=10)

            print("Lightroom에 성공적으로 연결됨!")

            lightroom.wrapper_object().maximize()
            lightroom.wrapper_object().set_focus()

            run_exports(lightroom=lightroom, check_stop_flag=self.check_stop_flag)

            self.check_stop_flag(context="작업관리자 실행으로 자동화 중단")

            self.check_stop_flag()

            print("Lightroom 자동화 완료")
            self.finished.emit(True)

            if self.lock_user_input == True or self.stop_flag == True:
                unlock_mouse_keyboard()

        except Exception as e:
            error_message = f"Lightroom 자동화 실패: {str(e)}"
            print(error_message)
            log_exception_to_file(exception_obj=e, message=error_message)
            self.failed.emit(True)
        except:
            print("Lightroom 자동화 실패: 알 수 없는 오류 발생")
            log_exception_to_file(exception_obj=None, message="Lightroom 자동화 중 알 수 없는 오류 발생")
            self.failed.emit(True)
