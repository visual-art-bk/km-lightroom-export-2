import re
import subprocess
import time
import psutil
import pygetwindow as gw  # ✅ 창을 제어하기 위한 라이브러리
from PySide6.QtCore import QThread, Signal
from helpers import log_exception_to_file

class LightroomLaunchThread(QThread):
    """Lightroom 실행을 담당하는 스레드"""

    lightroom_started = Signal(bool)  # ✅ Lightroom 실행 완료 여부 신호

    def run(self):
        print("🚀 Lightroom 실행 준비...")

        try:
            # ✅ 이미 실행 중인지 확인
            if self.is_lightroom_running():
                print("🔍 Lightroom이 이미 실행 중입니다. 창을 최대화합니다.")
                
                self.maximize_lightroom_window()  # ✅ 실행 중이면 최대화
                self.lightroom_started.emit(True)
                return
            
            print("🚀 Lightroom 실행 시작...")

            # ✅ 부모 프로세스와 완전히 독립적으로 실행되도록 설정
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_SHOWMAXIMIZED  # ✅ 실행 시 창을 최대화
            
            process = subprocess.Popen(
                [r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe"],
                startupinfo=startupinfo,
                creationflags=subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP,  # ✅ 부모 프로세스와 완전히 독립적으로 실행
                close_fds=True,  # ✅ 부모 프로세스와 연결된 파일 디스크립터를 닫음
                shell=False,
            )

            # ✅ Lightroom 실행될 때까지 대기
            for _ in range(30):  # 최대 30초 대기
                if self.is_lightroom_running():
                    print("✅ Lightroom 실행 감지됨! (창 최대화)")
                    self.maximize_lightroom_window()  # ✅ 실행 후 창을 최대화
                    self.lightroom_started.emit(True)
                    return
                time.sleep(1)

            print("❌ Lightroom 실행 감지 실패!")
            self.lightroom_started.emit(False)

        except Exception as e:
            print(f"❌ Lightroom 실행 실패: {e}")
            log_exception_to_file(exception_obj=e, message='Lightroom 실행 실패')
            self.lightroom_started.emit(False)

    def is_lightroom_running(self):
        """Lightroom이 실행 중인지 확인"""

        for process in psutil.process_iter(attrs=["name"]):
            if "Lightroom.exe" in process.info["name"]:
                return True
        return False

    def maximize_lightroom_window(self):
        """Lightroom 창을 정확하게 찾아서 최대화"""
        try:
            time.sleep(2)  # ✅ Lightroom 창이 완전히 로드될 때까지 대기

            # ✅ 모든 창 제목 가져오기
            all_windows = gw.getAllTitles()
            print(f"🔍 현재 실행 중인 창 목록: {all_windows}")

            # ✅ Lightroom 창 제목을 정규표현식으로 탐지
            pattern = r"Lightroom Catalog - Adobe (Photoshop )?Lightroom Classic - .*"
            lightroom_window = None

            for window_title in all_windows:
                if re.match(pattern, window_title):
                    lightroom_window = gw.getWindowsWithTitle(window_title)[0]
                    break

            if lightroom_window:
                if lightroom_window.isMinimized:
                    print("🔄 Lightroom 창이 최소화 상태, 복구 중...")
                    lightroom_window.restore()  # 창 복구
                
                print("🖥 Lightroom 창을 최대화합니다.")
                lightroom_window.maximize()
            else:
                print("⚠️ Lightroom 창을 찾을 수 없습니다.")
                log_exception_to_file(message='Lightroom 창을 찾을 수 없습니다.')

        except Exception as e:
            print(f"⚠️ Lightroom 창 최대화 실패: {e}")
            log_exception_to_file(exception_obj=e, message='Lightroom 창 최대화 실패')
            self.lightroom_started.emit(False)


    def minimize_lightroom_window(self):
        """Lightroom 창을 정확하게 찾아서 최소화"""
        try:
            time.sleep(2)  # ✅ Lightroom 창이 완전히 로드될 때까지 대기

            # ✅ 모든 창 제목 가져오기
            all_windows = gw.getAllTitles()
            print(f"🔍 현재 실행 중인 창 목록: {all_windows}")

            # ✅ Lightroom 창 제목을 정규표현식으로 탐지
            pattern = r"Lightroom Catalog - Adobe (Photoshop )?Lightroom Classic - .*"
            lightroom_window = None

            for window_title in all_windows:
                if re.match(pattern, window_title):
                    lightroom_window = gw.getWindowsWithTitle(window_title)[0]
                    break

            if lightroom_window:
                if not lightroom_window.isMinimized:
                    print("🖥 Lightroom 창을 최소화합니다.")
                    lightroom_window.minimize()
                else:
                    print("🔄 Lightroom 창이 이미 최소화 상태입니다.")
            else:
                print("⚠️ Lightroom 창을 찾을 수 없습니다.")
                log_exception_to_file(message='Lightroom 창을 찾을 수 없습니다.')

        except Exception as e:
            print(f"⚠️ Lightroom 창 최소화 실패: {e}")
            log_exception_to_file(exception_obj=e, message='Lightroom 창 최소화 실패')
            self.lightroom_started.emit(False)