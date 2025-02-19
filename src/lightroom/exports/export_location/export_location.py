from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_toggle import check_toggle
from lightroom.utils.check_main_menu import check_main_menu

# def set_desktop_folder(
#     export_window: WindowSpecification, collapsible_selection: WindowSpecification
# ):
#     select_btn = collapsible_selection.child_window(
#         title="선택...", control_type="Button"
#     )
#     select_btn.click_input()

#     desktop_path = export_window.child_window(
#         title_re=".*고정됨.*", control_type="TreeItem", found_index=0
#     )
#     desktop_path.click_input()

#     folder_name_edit = export_window.child_window(
#         title="폴더:", control_type="Edit", found_index=0
#     )
#     folder_name_edit.set_text("")
#     folder_name_edit.set_text("사진 저장")

#     folder_select_btn = export_window.child_window(
#         title="폴더 선택", control_type="Button", found_index=0
#     )
#     folder_select_btn.click_input()


MAIN_TITLE = "내보내기 위치"


def export_location(export_window: WindowSpecification, app_state, check_stop_flag):
    win_specs = check_main_menu(export_window=export_window, main_title=MAIN_TITLE)

    collapsible_selection = win_specs["col"]
    export_opt_of_window = win_specs["main_menu"]

    if check_stop_flag("[내보내기 위치] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    combobox = select_ui(
        win_specs=collapsible_selection,
        title="내보낼 위치:",
        control_type="ComboBox",
        found_index=0,
    )

    if check_stop_flag("[내보내기 위치] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    combobox.select("특정 폴더")

    checkbox_sub_folder = select_ui(
        title="하위 폴더에 넣기:",
        control_type="CheckBox",
        win_specs=export_window,
    )

    if check_stop_flag("[내보내기 위치] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    toggle_state = check_toggle(win_specs=checkbox_sub_folder)
    if toggle_state == False:
        checkbox_sub_folder.click()


    edit_field = export_window.child_window(control_type="Edit", found_index=0)
    if check_stop_flag("[내보내기 위치] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    edit_field.set_text(f"{app_state.username}{app_state.phone_number}")

    export_opt_of_window.click_input()
