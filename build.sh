cd C:\Users\YourUsername\Projects\LightroomController  # 경로 변경
pyinstaller --onedir --noupx --name="다비 내보내기 매니저" `
    --noconsole --noconfirm --clean `
    --hidden-import=PySide6 `
    --hidden-import=pywinauto `
    src/main.py
