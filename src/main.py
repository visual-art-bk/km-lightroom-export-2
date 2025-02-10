import sys
import pygetwindow as gw
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QLockFile, QDir
from ui.MainWindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ✅ QLockFile을 사용하여 중복 실행 방지
    lock_file = QLockFile(QDir.tempPath() + "/dabie_export.lock")

    if not lock_file.tryLock(100):
        # 이미 실행 중인 경우 기존 창 활성화
        windows = gw.getWindowsWithTitle("다비 내보내기 베타 V.1.0")
        if windows:
            window = windows[0]
            if window.isMinimized:
                window.restore()
            window.activate()
        sys.exit(0)

    # ✅ MainWindow 생성
    main_window = MainWindow(overlay_mode=True, lock_user_input=True, y=100)
    main_window.show()

    # ✅ 메인 윈도우가 숨겨져도 프로그램이 종료되지 않도록 유지
    app.exec()
