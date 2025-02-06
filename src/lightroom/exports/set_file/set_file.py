from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_collapsible_menu import check_collapsible_menu


def set_file(export_window: WindowSpecification):
    set_file = select_ui(
        win_specs=export_window,
        control_type="Pane",
        title="파일 설정",
        found_index=0,
    )
    collapsible = check_collapsible_menu(win_specs=export_window)

    if collapsible == None:
        print("콜랩서블 메뉴 존재X => 파일설정정 옵션 메뉴 클릭시작.")
        set_file.click_input()

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
