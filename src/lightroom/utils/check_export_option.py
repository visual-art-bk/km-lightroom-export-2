from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui


def check_export_option(win_specs: WindowSpecification, export_opt_title):

    collapsible_selection = win_specs.child_window(
        found_index=0,
        control_type="Pane",
        title="Collapsible Section",
    )

    export_opt = select_ui(
        title=export_opt_title,
        control_type="Pane",
        found_index=0,
        win_specs=collapsible_selection,
    )
    
    return collapsible_selection, export_opt