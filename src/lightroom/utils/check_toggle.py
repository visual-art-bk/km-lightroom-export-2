from pywinauto import WindowSpecification


def check_toggle(win_specs: WindowSpecification):
    state = win_specs.wrapper_object().get_toggle_state()

    return True if state == 1 else False
