from pywinauto import WindowSpecification
from lightroom.utils.close_needless_menu import close_needless_menu


MAIN_TITLE = "Content Credentials(얼리 액세스)"


def collapse_credentials_opt(export_window: WindowSpecification):
    close_needless_menu(export_window=export_window, main_title=MAIN_TITLE)
