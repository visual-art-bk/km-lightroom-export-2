from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui


def set_file(export_window: WindowSpecification):
    try:
        # 내보내기 위치 메뉴 찾고 클릭
        set_file = select_ui(
            win_specs=export_window,
            control_type="Pane",
            title="파일 설정",
            found_index=0,
        )
        set_file.click_input()

        set_file.print_control_identifiers()

    except Exception:
        print("파일 이름 지정이이 열려있음 다음으로 넘어갑니다.")

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

    set_file.click_input()
