from pywinauto import  WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_export_option import check_export_option
from lightroom.utils.check_toggle import check_toggle


def specs_filename(export_window: WindowSpecification):
    
    (
        collapsible_selection,
        export_opt_of_col,
    ) = check_export_option(win_specs=export_window, export_opt_title="파일 이름 지정")
    
    export_opt_of_window = select_ui(
            win_specs=export_window,
            control_type="Pane",
            title="파일 이름 지정",
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

    checkbox = select_ui(
        control_type="CheckBox",
        title="바꿀 이름:",
        win_specs=collapsible_selection,
    )
    toggle_state = check_toggle(win_specs=checkbox)
    if toggle_state == False:
        checkbox.click()

    combobox = collapsible_selection.child_window(
        control_type="ComboBox", found_index=0
    )
    combobox.select("사용자 정의 이름 - 시퀀스")

    edit_field = select_ui(
        control_type="Edit",
        title="사용자 정의 텍스트:",
        win_specs=collapsible_selection,
        found_index=0,
    )

    edit_field.set_text("")
    edit_field.set_text("필터")

    export_opt_of_window.click_input()
