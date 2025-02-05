import time
from pywinauto import WindowSpecification
from lightroom.exports.finds.get_ui_export_location_combo import (
    get_ui_export_location_combo,
)
from lightroom.utils.select_ui import select_ui
from lightroom.utils.get_state_legacy import get_state_legacy

KEYS_SELECT_ALL = "^a"
KEYS_SELECT_EXPORT = "^+E"
CONTROL_TYPE_FILE_MENU = "MenuItem"
CONTROL_TYPE_CHECKBOX = "CheckBox"
CONTROL_TYPE_EXPORT_PATH = "Button"
TITLE_FILE_MENU = "파일(F)"
TITLE_SUB_FOLDER = "하위 폴더에 넣기:"
TITLE_EXPORT_PATH = "열기"
TEXT_DESKTOP = "특정 폴더"


def toggle_checkbox(win_specs: WindowSpecification):
    current_state = get_state_legacy(win_specs=win_specs)
    if current_state != 1:
        print("체크박스 상태:", "✅ 체크됨" if current_state == 1 else "❌ 체크 안됨")
        win_specs.toggle()
        return


def export_location(export_window: WindowSpecification, app_state):
    # 내보내기 위치 자동화
    ui_export_location_combo = get_ui_export_location_combo(win_specs=export_window)
    # 위치 콤보박스에서 바탕화면 선택
    ui_export_location_combo.select(TEXT_DESKTOP)

    # 하위 폴더에 넣기 요소
    checkbox_sub_folder = select_ui(
        control_type=CONTROL_TYPE_CHECKBOX,
        title=TITLE_SUB_FOLDER,
        win_specs=export_window,
    )

    # 하위 폴더 넣기 체크박스
    toggle_checkbox(win_specs=checkbox_sub_folder)

    edit_field = export_window.child_window(control_type="Edit", found_index=0)

    time.sleep(1)
    edit_field.set_text("")
    edit_field.set_text(f"{app_state.username}{app_state.phone_number}")
