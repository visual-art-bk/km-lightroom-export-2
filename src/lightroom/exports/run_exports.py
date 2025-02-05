import time
from pywinauto import Application, WindowSpecification
from lightroom.exports.selects.open_export_window import open_export_window
from lightroom.exports.selects.select_all_imgs import select_all_imgs
from lightroom.exports.finds.get_ui_export_location_combo import (
    get_ui_export_location_combo,
)
from lightroom.utils.select_ui import select_ui
from lightroom.utils.send_shortcuts import send_shortcuts
from lightroom.utils.get_state_legacy import get_state_legacy
from state_manager.StateManager import StateManager
from lightroom.exports.export_location.export_location import export_location

KEYS_SELECT_ALL = "^a"
KEYS_SELECT_EXPORT = "^+E"
CONTROL_TYPE_FILE_MENU = "MenuItem"
CONTROL_TYPE_CHECKBOX = "CheckBox"
CONTROL_TYPE_EXPORT_PATH = "Button"
TITLE_FILE_MENU = "파일(F)"
TITLE_SUB_FOLDER = "하위 폴더에 넣기:"
TITLE_EXPORT_PATH = "열기"
TEXT_DESKTOP = "특정 폴더"




def run_exports(lightroom: WindowSpecification):
    state_manager = StateManager()
    app_state = state_manager.get_state()

    # TODO
    # select_all_imgs(win_specs=lightroom)

    # 전체 사진 단축키로 선택
    send_shortcuts(
        keys=KEYS_SELECT_ALL,
        context="전체 사진 선택 Ctrl + A 실행",
        win_specs=lightroom,
    )

    # 파일 메뉴 열기
    select_ui(
        control_type=CONTROL_TYPE_FILE_MENU,
        title=TITLE_FILE_MENU,
        win_specs=lightroom,
    )

    # 내보내기 단축키로 누르기
    send_shortcuts(
        keys=KEYS_SELECT_EXPORT,
        context=f"내보내기 단축키 {KEYS_SELECT_EXPORT}",
        win_specs=lightroom,
    )

    # 내보내기 단축키로 활성화
    export_window = open_export_window(lightroom=lightroom)
    
    export_location(export_window=export_window, app_state=app_state)



    export_button = export_window.child_window(
        title="내보내기", auto_id="1", control_type="Button"
    )

    export_button.click_input()
