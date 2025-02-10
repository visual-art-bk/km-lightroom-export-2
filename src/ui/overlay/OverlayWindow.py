from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtCore import Qt, Signal


class OverlayWindow(QWidget):
    """배경 역할을 하는 오버레이 창"""

    _instance = None  # 싱글턴 패턴 적용
    overlay_closed = Signal()  # ✅ 오버레이가 닫힐 때 신호를 발생

    def __init__(
        self,
        width=500,
        height=250,
        bg_color="#0000FF",  
        text_color="yellow",  
        font_size=30,
        animation_speed=20,
        y_offset=100,  
        opacity=0.5,  
        blur_radius=10,  
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.y_offset = y_offset  
        self.bg_color = bg_color  
        self.opacity = opacity  
        self.animation_speed = animation_speed
        self.blur_radius = blur_radius  

        self.setWindowTitle("오버레이 창")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        # ✅ 닫기 버튼 추가 (오버레이 종료용)
        self.close_button = QPushButton("✖", self)
        self.close_button.setGeometry(self.width - 35, 10, 25, 25)
        self.close_button.setStyleSheet(
            "background: none; border: none; color: white; font-size: 18px; font-weight: bold;"
        )
        self.close_button.clicked.connect(self.close_overlay)

        # ✅ 창 중앙 정렬
        self.center_window()

    def center_window(self):
        """창을 화면 좌우 정가운데 위치시키고, 위아래(Y축)는 사용자 지정"""
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        x_pos = (screen_width - self.width) // 2  
        y_pos = min(max(self.y_offset, 0), screen_height - self.height)  

        self.setGeometry(x_pos, y_pos, self.width, self.height)

    @classmethod
    def create_overlay(cls, **kwargs):
        """싱글턴 방식으로 오버레이 창을 생성"""
        if cls._instance is None:
            cls._instance = OverlayWindow(**kwargs)
        return cls._instance

    def close_overlay(self):
        """✅ 닫기 버튼 클릭 시 오버레이 창을 닫음"""
        print("닫기 버튼을 클릭했습니다.")  
        self.overlay_closed.emit()  # ✅ 신호 발생 (MainWindow에서 받을 것)
        self.close()  
        self.deleteLater()  
        OverlayWindow._instance = None  
