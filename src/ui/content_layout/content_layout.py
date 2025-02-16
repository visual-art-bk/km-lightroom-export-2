from PySide6.QtWidgets import QGridLayout
from PySide6.QtCore import Qt
from ui.content_layout.TextContainerWidget import TextContainerWidget


def content_layout(height):
    """✅ 안내메시지를 불러와 TextContainerWidget을 중앙에 배치하는 레이아웃"""
    file_path = "오버레이메세지.txt"  # 루트 디렉토리에 있는 파일에서 불러옴
    text_container = TextContainerWidget(file_path=file_path, font_sizes=20, text_color="black", height=height)

    # layout = QGridLayout()
    # layout.setContentsMargins(0, 0, 0, 0)
    # layout.setAlignment(Qt.AlignCenter)
    # layout.addWidget(text_container, 0, 0, Qt.AlignCenter)

    return text_container
