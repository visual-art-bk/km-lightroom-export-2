from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_export_option import check_export_option
from lightroom.utils.check_toggle import check_toggle


def img_size_adjust(export_window: WindowSpecification):

    (
        collapsible_selection,
        export_opt_of_col,
    ) = check_export_option(
        win_specs=export_window, export_opt_title="이미지 크기 조정"
    )

    export_opt_of_window = select_ui(
        win_specs=export_window,
        control_type="Pane",
        title="이미지 크기 조정",
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
        win_specs=collapsible_selection,
        control_type="CheckBox",
        found_index=0,
        title="크기 조정하여 맞추기:",
    )
    toggle_state = check_toggle(win_specs=checkbox)
    if toggle_state == False:
        checkbox.click()

    edit_width = select_ui(
        win_specs=collapsible_selection,
        control_type="Edit",
        found_index=0,
        title="%",
    )

    edit_width.set_text("")
    edit_width.set_text("2456")

    edit_height = select_ui(
        win_specs=collapsible_selection,
        control_type="Edit",
        found_index=0,
        title="높이:",
    )

    edit_height.set_text("")
    edit_height.set_text("4000")

    resolution = select_ui(
        win_specs=collapsible_selection,
        control_type="Edit",
        found_index=0,
        title="해상도:",
    )

    resolution.set_text("")
    resolution.set_text("360")

    # 토글 대신
    export_opt_of_window.click_input()
