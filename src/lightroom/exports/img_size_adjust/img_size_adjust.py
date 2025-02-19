from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_main_menu import check_main_menu
from lightroom.utils.check_toggle import check_toggle

MAIN_TITLE = "이미지 크기 조정"


def img_size_adjust(export_window: WindowSpecification, check_stop_flag):
    win_specs = check_main_menu(export_window=export_window, main_title=MAIN_TITLE)

    collapsible_selection = win_specs["col"]
    export_opt_of_window = win_specs["main_menu"]

    if check_stop_flag("[이미지 크기 조정] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    checkbox = select_ui(
        win_specs=collapsible_selection,
        control_type="CheckBox",
        found_index=0,
        title="크기 조정하여 맞추기:",
    )
    toggle_state = check_toggle(win_specs=checkbox)
    if toggle_state == False:
        checkbox.click()

    if check_stop_flag("[이미지 크기 조정] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    edit_width = select_ui(
        win_specs=collapsible_selection,
        control_type="Edit",
        found_index=0,
        title="%",
    )

    edit_width.set_text("2456")

    if check_stop_flag("[이미지 크기 조정] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    edit_height = select_ui(
        win_specs=collapsible_selection,
        control_type="Edit",
        found_index=0,
        title="높이:",
    )

    edit_height.set_text("4000")

    if check_stop_flag("[이미지 크기 조정] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    resolution = select_ui(
        win_specs=collapsible_selection,
        control_type="Edit",
        found_index=0,
        title="해상도:",
    )

    resolution.set_text("160")

    export_opt_of_window.click_input()
