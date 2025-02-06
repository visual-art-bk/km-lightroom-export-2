import time
from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_collapsible_menu import check_collapsible_menu
from lightroom.utils.check_toggle import check_toggle

KEYS_SELECT_ALL = "^a"
KEYS_SELECT_EXPORT = "^+E"
CONTROL_TYPE_FILE_MENU = "MenuItem"
CONTROL_TYPE_CHECKBOX = "CheckBox"
CONTROL_TYPE_EXPORT_PATH = "Button"
TITLE_FILE_MENU = "파일(F)"
TITLE_SUB_FOLDER = "하위 폴더에 넣기:"
TITLE_EXPORT_PATH = "열기"
TEXT_DESKTOP = "특정 폴더"


def export_location(export_window: WindowSpecification, app_state):
    export_path = select_ui(
        win_specs=export_window,
        control_type="Pane",
        title="내보내기 위치",
        found_index=0,
    )

    collapsible = check_collapsible_menu(win_specs=export_window)

    if collapsible == None:
        print("콜랩서블 메뉴 존재X => 내보내기 옵션 메뉴 클릭시작.")
        export_path.click()

    collapsible_selection = check_collapsible_menu(win_specs=export_window)

    combobox = select_ui(
        win_specs=collapsible_selection,
        title="내보낼 위치:",
        control_type="ComboBox",
        found_index=0,
    )

    combobox.select(TEXT_DESKTOP)

    checkbox_sub_folder = select_ui(
        control_type=CONTROL_TYPE_CHECKBOX,
        title=TITLE_SUB_FOLDER,
        win_specs=export_window,
    )


    toggle_state = check_toggle(win_specs=checkbox_sub_folder)
    if toggle_state == False:
        checkbox_sub_folder.click()

    edit_field = export_window.child_window(control_type="Edit", found_index=0)

    time.sleep(1)
    edit_field.set_text("")
    edit_field.set_text(f"{app_state.username}{app_state.phone_number}")

    export_path.click_input()
