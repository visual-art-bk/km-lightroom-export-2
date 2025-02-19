from pywinauto import WindowSpecification
from lightroom.utils.close_needless_menu import close_needless_menu


MAIN_TITLE = "Content Credentials(얼리 액세스)"


def collapse_credentials_opt(export_window: WindowSpecification, check_stop_flag):
    if check_stop_flag("[이미지 크기 조정] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    close_needless_menu(export_window=export_window, main_title=MAIN_TITLE)
