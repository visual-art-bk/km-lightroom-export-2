from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_main_menu import check_main_menu
from lightroom.utils.check_toggle import check_toggle

MAIN_TITLE = "파일 이름 지정"


def specs_filename(export_window: WindowSpecification, check_stop_flag):
    win_specs = check_main_menu(export_window=export_window, main_title=MAIN_TITLE)

    collapsible_selection = win_specs["col"]
    export_opt_of_window = win_specs["main_menu"]

    if check_stop_flag(
        "[파일이름 지정하기기] 자동화화 전 작업관리자 실행으로 자동화 중단"
    ):
        return False
    collapsible_selection = select_ui(
        found_index=0,
        control_type="Pane",
        title="Collapsible Section",
        win_specs=export_window,
    )

    checkbox = select_ui(
        control_type="CheckBox",
        title="바꿀 이름:",
        win_specs=collapsible_selection,
    )

    if check_stop_flag(
        "[파일이름 지정하기기] 자동화화 전 작업관리자 실행으로 자동화 중단"
    ):
        return False
    toggle_state = check_toggle(win_specs=checkbox)
    if toggle_state == False:
        checkbox.click()

    combobox = collapsible_selection.child_window(
        control_type="ComboBox", found_index=0
    )

    if check_stop_flag(
        "[파일이름 지정하기기] 자동화화 전 작업관리자 실행으로 자동화 중단"
    ):
        return False
    combobox.select("사용자 정의 이름 - 시퀀스")

    edit_field = select_ui(
        control_type="Edit",
        title="사용자 정의 텍스트:",
        win_specs=collapsible_selection,
        found_index=0,
    )

    if check_stop_flag(
        "[파일이름 지정하기기] 자동화화 전 작업관리자 실행으로 자동화 중단"
    ):
        return False
    edit_field.set_text("필터")

    export_opt_of_window.click_input()
