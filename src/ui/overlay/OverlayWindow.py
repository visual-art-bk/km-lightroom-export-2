from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal
from ui.buttons.close_btn import close_btn
from ui.content_layout.content_layout import content_layout
from ui.effects.ImageSlideshow import ImageSlideshow


class OverlayWindow(QWidget):
    overlay_closed = Signal()

    def __init__(self):
        super().__init__(None)  # 부모 없음 (독립 창)

        self.overlay_width = 1050
        self.overlay_height = 250
        self.init_position()  # 창 위치 초기화

        # ✅ 배경 투명 설정
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

        self.setup_layout()

    def set_btn_close(self, overlay_container):
        if overlay_container == None:
            raise ValueError("overlay_container가 초기화되지 않았음")
        btn_close = close_btn()
        btn_close.setParent(overlay_container)
        btn_close.move(self.overlay_width - 40, 10)
        btn_close.clicked.connect(self.close_overlay)

    def set_overlay_layout(self):
        slideshow = ImageSlideshow(
            width=self.overlay_width,
            height=self.overlay_height,
            aspect_ratio_mode=Qt.KeepAspectRatioByExpanding,
        )
        slideshow.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )  # ✅ 크기 자동 조정
        # 안내 가이드 UI, 현재 슬라이드가 대체함.
        # guide_contents = content_layout(height=self.overlay_height)

        overlay_container = QWidget(self)
        overlay_container.setObjectName("overlayContainer")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(slideshow)

        overlay_container.setLayout(layout)
        overlay_container.setGeometry(0, 0, self.overlay_width, self.overlay_height)

        return overlay_container

    def close_overlay(self):
        """✅ 오버레이 닫고 부모 윈도우에 신호 전달"""
        self.overlay_closed.emit()
        self.close()

    def init_position(self):
        """✅ 창을 화면 좌우 정중앙에 위치"""
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        x_pos = (screen_width - self.overlay_width) // 2
        y_pos = 18  # 고정된 Y축 위치
        self.setGeometry(x_pos, y_pos, self.overlay_width, self.overlay_height)

    def setup_layout(self):
        """전체 UI 레이아웃 설정"""
        overlay_container = self.set_overlay_layout()

        self.set_btn_close(overlay_container)  # Absolute postin 효과를 위해 나중에 추가

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(overlay_container)

        self.setLayout(main_layout)
