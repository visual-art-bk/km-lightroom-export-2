import subprocess
import time
import psutil
from PySide6.QtCore import QThread, Signal
from helpers import log_exception_to_file

# ✅ Windows 상수 정의
SW_SHOWMAXIMIZED = 3  # Maximized 상태로 표시

class LightroomLaunchThread(QThread):
    """Lightroom 실행을 담당하는 스레드"""

    lightroom_started = Signal(bool)  # ✅ Lightroom 실행 완료 여부 신호

    def run(self):
        print("🚀 Lightroom 실행 준비...")

        try:
            # ✅ Lightroom Classic 무조건 실행
            print("🚀 Lightroom Classic 실행 시작...")

            # ✅ 부모 프로세스와 완전히 독립적으로 실행되도록 설정
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = SW_SHOWMAXIMIZED  # ✅ 실행 시 창을 최대화

            # ✅ Lightroom Classic 실행
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
                    print("✅ Lightroom 실행 감지됨!")
                    self.lightroom_started.emit(True)
                    return
                time.sleep(1)

            print("❌ Lightroom 실행 감지 실패!")
            self.lightroom_started.emit(False)

        except Exception as e:
            print(f"❌ Lightroom 실행 실패: {e}")
            log_exception_to_file(exception_obj=e, message="Lightroom 실행 실패")
            self.lightroom_started.emit(False)

    def is_lightroom_running(self):
        """Lightroom이 실행 중인지 확인"""
        for process in psutil.process_iter(attrs=["name"]):
            if "Lightroom.exe" in process.info["name"]:
                return True
        return False
