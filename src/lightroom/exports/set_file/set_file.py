from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_main_menu import check_main_menu

MAIN_TITLE="파일 설정"

def set_file(export_window: WindowSpecification):
    win_specs = check_main_menu(export_window=export_window, main_title=MAIN_TITLE)

    collapsible_selection = win_specs["col"]
    export_opt_of_window = win_specs["main_menu"]

    combobox = select_ui(
        win_specs=collapsible_selection,
        control_type="ComboBox",
        found_index=0,
        title="이미지 형식:",
    )
    combobox.select("JPEG")

    edit_field = collapsible_selection.child_window(
        auto_id="65535",
        control_type="Edit",
        found_index=0,
    )
    
    edit_field.set_text("90")

    export_opt_of_window.click_input()
