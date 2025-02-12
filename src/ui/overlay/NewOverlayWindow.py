from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
)
from PySide6.QtCore import Qt, Signal
from ui.overlay.TextContainerWidget import TextContainerWidget
from ui.overlay.text_contents import text_contents


class NewOverlayWindow(QWidget):
    # ✅ 부모 윈도우와 통신할 시그널 정의
    overlay_closed = Signal()  # 오버레이가 닫힐 때 부모에게 알리는 시그널

    def __init__(self):
        super().__init__(None)  # ✅ 부모 없음 (독립적인 창)

        # ✅ 창 크기 지정 (초기화 시 크기를 미리 설정)
        self.overlay_width = 400
        self.overlay_height = 200
        self.setFixedSize(self.overlay_width, self.overlay_height)  # ✅ 크기 고정

        # ✅ 독립적인 팝업 창으로 설정
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        # ✅ 부모(오버레이)에만 보더 적용 & 자식들에게 상속 방지
        self.setObjectName("overlayContainer")  # ✅ QWidget에 특정 ID 부여
        self.setStyleSheet(
            """
            QWidget#overlayContainer {
                background-color: rgba(255, 237, 243, 1);
            }
            QPushButton {
                border: none;  /* ✅ 닫기 버튼에 보더 없애기 */
            }
        """
        )

        self.init_appearance()  # ✅ 창 위치 초기화

        # ✅ 전체 레이아웃 (겹쳐서 배치 가능하도록 설정)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # ✅ 마진 제거하여 UI를 꽉 차게 정렬

        # ✅ 닫기 버튼 (상단 오른쪽 고정)
        close_button = QPushButton("✖")
        close_button.setFixedSize(30, 30)  # ✅ 버튼 크기 설정
        close_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                font-size: 16px;
                color: black;
            }
            QPushButton:hover {
                color: red;
                font-weight: bold;
            }
        """
        )  # ✅ CSS 적용 (호버 시 빨간색 강조)
        close_button.clicked.connect(self.close_overlay)  # ✅ 버튼 클릭 시 닫기

        # ✅ 닫기 버튼을 오버레이 상단 오른쪽에 겹치도록 배치
        close_layout = QHBoxLayout()
        close_layout.setContentsMargins(0, 0, 0, 0)  # ✅ 마진 없애기
        close_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)  # ✅ 오른쪽 상단 정렬
        close_layout.addWidget(close_button)

        # ✅ 텍스트 컨텐츠 (정확한 중앙 정렬)
        content_layout = QGridLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setAlignment(Qt.AlignCenter)  # ✅ 전체 중앙 정렬

        text_container = TextContainerWidget(
            text_contents=text_contents,
            font_sizes=20,
            text_color="black",
            height=self.overlay_height,  # ✅ 올바른 높이 전달
        )
        content_layout.addWidget(text_container, 0, 0, Qt.AlignCenter)  # ✅ 정중앙 배치

        # ✅ 전체 레이아웃 구성 (닫기 버튼을 텍스트 위로 겹치게 설정)
        overlay_container = QWidget(self)
        overlay_container.setObjectName("overlayContainer")  # ✅ ID 설정
        overlay_container.setLayout(content_layout)  # ✅ 텍스트를 포함한 위젯
        overlay_container.setGeometry(
            0, 0, self.overlay_width, self.overlay_height
        )  # ✅ 크기 설정

        close_button.setParent(
            overlay_container
        )  # ✅ 닫기 버튼을 부모 위젯과 겹치도록 설정
        close_button.move(
            self.overlay_width - 40, 10
        )  # ✅ 닫기 버튼을 오른쪽 상단으로 이동

        main_layout.addWidget(overlay_container)  # ✅ 오버레이 전체 추가
        self.setLayout(main_layout)

    def close_overlay(self):
        """✅ 오버레이 닫고 부모 윈도우에 신호 전달"""
        self.overlay_closed.emit()  # ✅ 시그널 발생 → 부모에게 알림
        self.close()

    def init_appearance(self):
        """✅ 창을 화면 좌우 정중앙 위치시키고, 위아래(Y축)는 사용자 지정"""
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()

        # ✅ 창 너비를 먼저 설정한 후, 정확한 중앙 위치 계산
        x_pos = (screen_width - self.overlay_width) // 2  # ✅ 정확한 창 너비 사용
        y_pos = 18  # ✅ 고정된 Y축 위치

        self.setGeometry(
            x_pos, y_pos, self.overlay_width, self.overlay_height
        )  # ✅ 위치 및 크기 적용
