from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_export_option import check_export_option


def set_file(export_window: WindowSpecification):
    
    (
        collapsible_selection,
        export_opt_of_col,
    ) = check_export_option(win_specs=export_window, export_opt_title="파일 설정")
    
    export_opt_of_window = select_ui(
            win_specs=export_window,
            control_type="Pane",
            title="파일 설정",
            found_index=0,
        )

    if export_opt_of_col == None:
        export_opt_of_window.click_input()
 

    collapsible_selection = select_ui(
        found_index=0,
        control_type="Pane",
        title="Collapsible Section",
        win_specs=export_window,
    )

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
    edit_field.set_text("")
    edit_field.set_text("90")

    export_opt_of_window.click_input()
