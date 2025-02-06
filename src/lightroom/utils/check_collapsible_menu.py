from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui


def check_collapsible_menu(win_specs: WindowSpecification):
    try:
        collapsible_selection = select_ui(
            found_index=0,
            control_type="Pane",
            title="Collapsible Section",
            win_specs=win_specs,
        )
    except:
        print("콜랩서블 메뉴 없음.")

    finally:
        return collapsible_selection
