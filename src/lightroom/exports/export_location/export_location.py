import time
from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_export_option import check_export_option
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

    (
        collapsible_selection,
        export_opt_of_col,
    ) = check_export_option(win_specs=export_window, export_opt_title="내보내기 위치")
    
    export_opt_of_window = select_ui(
            win_specs=export_window,
            control_type="Pane",
            title="내보내기 위치",
            found_index=0,
        )
    
    if export_opt_of_col == None:
        export_opt_of_window.click_input()
      
        
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

    export_opt_of_window.click_input()
