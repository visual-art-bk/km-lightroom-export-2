from PySide6.QtWidgets import QPushButton


def close_btn(parent):
    close_btn = QPushButton("✖", parent)
    close_btn.setGeometry(parent.width - 35, 10, 25, 25)
    close_btn.setStyleSheet(
        "background: none; border: none; color: black; font-size: 18px; font-weight: bold;"
    )
    return close_btn
