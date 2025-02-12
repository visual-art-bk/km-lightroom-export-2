import time
from pywinauto import WindowSpecification


def select_ui(
    win_specs: WindowSpecification,
    title="정의되지않음",
    control_type="정의되지않음",
    timeout=0.1,
    found_index=None,
) -> WindowSpecification:

    print(f"---> [{title}] 메뉴 찾기 시작..")
    ui = None

    try:
        ui = win_specs.child_window(
            title=title, control_type=control_type, found_index=found_index
        )
        print(f"---> [{title}] 요소를 찾았습니다.")
        return ui
    except:
        print(f"---> !!! [{title}] 요소가 존재하지 않습니다.")

        return None