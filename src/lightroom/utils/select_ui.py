import time
from pywinauto import WindowSpecification


def select_ui(
    win_specs: WindowSpecification,
    title="정의되지않음",
    control_type="정의되지않음",
    timeout=0.1,
    found_index=0,
) -> WindowSpecification:

    print(f"{title} 메뉴 클릭 시작..")

    if found_index != 0:

        ui = win_specs.child_window(title=title, control_type=control_type)
    else:

        ui = win_specs.child_window(
            title=title, control_type=control_type, found_index=found_index
        )

        

    # # ✅ 5초 동안 0.5초 간격으로 메뉴 확인 → 즉시 감지 가능
    # for _ in range(10):
    #     if ui.exists():
    #         print(f"🚨 {title}  메뉴가 존재!")

    #         return ui
    #     time.sleep(timeout)

    # print(f"🚨 {title}  메뉴가 존재하지 않음!")
    return None
