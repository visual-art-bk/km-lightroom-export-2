from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
    QGraphicsOpacityEffect,
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QPixmap

DURATION_PLAY = 4250
DURATION_FADEIN = 850
DURATION_FADEOUT = 500


class ImageSlideshow(QWidget):
    def __init__(self, width, height):
        super().__init__()

        self.setFixedSize(width, height)

        # ✅ 여러 이미지를 담는 QStackedWidget
        self.stack = QStackedWidget(self)

        # ✅ 이미지 추가
        self.images = ["image1.jpg", "image2.jpg", "image3.jpg"]  # 이미지 경로
        self.labels = []
        self.effects = []  # ✅ 각 이미지의 투명도 효과 저장
        for img in self.images:
            label = QLabel()
            label.setPixmap(QPixmap(img).scaled(width, height, Qt.KeepAspectRatio))
            label.setAlignment(Qt.AlignCenter)

            # ✅ 투명도 효과 추가
            effect = QGraphicsOpacityEffect()
            label.setGraphicsEffect(effect)
            effect.setOpacity(0.0)  # 초기 투명도를 0으로 설정
            self.effects.append(effect)

            self.stack.addWidget(label)
            self.labels.append(label)

        # ✅ 처음 이미지만 보이도록 설정
        self.effects[0].setOpacity(1.0)
        self.stack.setCurrentIndex(0)

        # ✅ 전체 레이아웃
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)
        self.setLayout(layout)

        # ✅ 애니메이션 설정
        self.fade_out = QPropertyAnimation(self.effects[0], b"opacity")
        self.fade_out.setDuration(DURATION_FADEOUT)

        self.fade_in = QPropertyAnimation(self.effects[0], b"opacity")
        self.fade_in.setDuration(DURATION_FADEIN)

        # ✅ 타이머 설정 (3초마다 이미지 변경)
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_image)
        self.timer.start(DURATION_PLAY)

        self.current_index = 0

    def next_image(self):
        """다음 이미지로 변경하는 애니메이션"""
        old_index = self.current_index
        self.current_index = (self.current_index + 1) % len(self.labels)

        # ✅ 기존 이미지 페이드아웃 설정
        self.fade_out.setTargetObject(self.effects[old_index])
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)

        # ✅ 새 이미지 페이드인 설정 (애니메이션 완료 후 실행)
        self.fade_out.finished.connect(
            self.switch_image
        )  # ✅ 애니메이션이 끝나면 switch_image 실행
        self.fade_out.start()

    def switch_image(self):
        """이미지 변경 후 페이드인 실행"""
        self.stack.setCurrentIndex(self.current_index)  # ✅ 새 이미지로 변경

        self.fade_in.setTargetObject(self.effects[self.current_index])
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.start()
