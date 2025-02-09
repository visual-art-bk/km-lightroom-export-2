import time
from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_export_option import check_export_option
from lightroom.utils.check_toggle import check_toggle

CONTROL_TYPE_CHECKBOX = "CheckBox"
CONTROL_TYPE_EXPORT_PATH = "Button"
TITLE_FILE_MENU = "파일(F)"
TITLE_SUB_FOLDER = "하위 폴더에 넣기:"
TITLE_EXPORT_PATH = "열기"
TEXT_DESKTOP = "특정 폴더"


def set_desktop_folder(
    export_window: WindowSpecification, collapsible_selection: WindowSpecification
):
    select_btn = collapsible_selection.child_window(
        title="선택...", control_type="Button"
    )
    select_btn.click_input()

    desktop_path = export_window.child_window(
        title_re=".*고정됨.*", control_type="TreeItem", found_index=0
    )
    desktop_path.click_input()

    folder_name_edit = export_window.child_window(
        title="폴더:", control_type="Edit", found_index=0
    )
    folder_name_edit.set_text("")
    folder_name_edit.set_text("사진 저장")

    folder_select_btn = export_window.child_window(
        title="폴더 선택", control_type="Button", found_index=0
    )
    folder_select_btn.click_input()


def export_location(export_window: WindowSpecification, app_state):

    (
        collapsible_selection,
        export_opt_of_col,
    ) = check_export_option(win_specs=export_window, export_opt_title="내보내기 위치")

    export_opt_of_window = select_ui(
        win_specs=export_window,
        control_type="Pane",
        title="내보내기 위치",
        found_index=0,
    )

    if export_opt_of_col == None:
        export_opt_of_window.click_input()

    combobox = select_ui(
        win_specs=collapsible_selection,
        title="내보낼 위치:",
        control_type="ComboBox",
        found_index=0,
    )

    combobox.select(TEXT_DESKTOP)

    # 데스크탑에 저장하기
    # set_desktop_folder(
    #     collapsible_selection=collapsible_selection, export_window=export_window
    # )

    checkbox_sub_folder = select_ui(
        control_type=CONTROL_TYPE_CHECKBOX,
        title=TITLE_SUB_FOLDER,
        win_specs=export_window,
    )

    toggle_state = check_toggle(win_specs=checkbox_sub_folder)
    if toggle_state == False:
        checkbox_sub_folder.click()

    edit_field = export_window.child_window(control_type="Edit", found_index=0)

    time.sleep(1)
    edit_field.set_text("")
    edit_field.set_text(f"{app_state.username}{app_state.phone_number}")

    export_opt_of_window.click_input()
