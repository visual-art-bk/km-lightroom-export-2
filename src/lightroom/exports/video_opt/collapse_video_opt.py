from pywinauto import WindowSpecification
from lightroom.utils.close_needless_menu import close_needless_menu

MAIN_TITLE = "비디오"


def collapse_video_opt(export_window: WindowSpecification):
    close_needless_menu(export_window=export_window, main_title=MAIN_TITLE)
