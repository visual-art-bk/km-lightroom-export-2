import subprocess
import time
import psutil
import pygetwindow as gw  # ✅ 창을 제어하기 위한 라이브러리
from PySide6.QtCore import QThread, Signal

class LightroomLaunchThread(QThread):
    """Lightroom 실행을 담당하는 스레드"""

    lightroom_started = Signal(bool)  # ✅ Lightroom 실행 완료 여부 신호

    def run(self):
        """Lightroom 실행 (이미 실행 중이면 최대화, 아니면 실행 후 최대화)"""
        print("🚀 Lightroom 실행 중...")

        try:
            # ✅ 이미 실행 중인지 확인
            if self.is_lightroom_running():
                print("🔍 Lightroom이 이미 실행 중입니다. 창을 최대화합니다.")
                
                self.maximize_lightroom_window()  # ✅ 실행 중이면 최대화
                self.lightroom_started.emit(True)
                return
            
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
            self.lightroom_started.emit(False)

    def is_lightroom_running(self):
        """Lightroom이 실행 중인지 확인"""

        for process in psutil.process_iter(attrs=["name"]):
            print(process)
            print( process.info["name"] )
            
            if "Lightroom.exe" in process.info["name"]:
                return True
        return False

    def maximize_lightroom_window(self):
        """이미 실행 중인 Lightroom 창을 최대화"""
        try:
            for window in gw.getWindowsWithTitle("Lightroom"):
                if window and not window.isMaximized:

                    print("🖥 Lightroom 창을 최대화합니다.")
                    window.maximize()
                    return
        except Exception as e:
            print(f"⚠️ Lightroom 창 최대화 실패: {e}")
