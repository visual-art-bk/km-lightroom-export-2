from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_collapsible_menu import check_collapsible_menu


def img_size_adjust(export_window: WindowSpecification):
    size_adjust = select_ui(
        win_specs=export_window,
        control_type="Pane",
        title="이미지 크기 조정",
        found_index=0,
    )
    
    collapsible = check_collapsible_menu(win_specs=export_window)

    if collapsible == None:
        print("콜랩서블 메뉴 존재X => 사진 크기기 옵션 메뉴 클릭시작.")
        size_adjust.click_input()



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
    # 토글 대신
    checkbox.click_input()
    checkbox.click_input()

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
    size_adjust.click_input()
