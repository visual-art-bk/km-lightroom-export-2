from pywinauto import WindowSpecification, keyboard
from lightroom.exports.selects.open_export_window import open_export_window
from lightroom.utils.select_ui import select_ui
from lightroom.utils.send_shortcuts import send_shortcuts
from state_manager.StateManager import StateManager
from lightroom.exports.export_location.export_location import export_location
from lightroom.exports.specs_filename.specs_filename import specs_filename
from lightroom.exports.video_opt.collapse_video_opt import collapse_video_opt
from lightroom.exports.set_file.set_file import set_file
from lightroom.exports.img_size_adjust.img_size_adjust import img_size_adjust
from lightroom.exports.content_credentials_opt.collapse_credentials_opt import (
    collapse_credentials_opt,
)

KEYS_SELECT_ALL = "^a"
KEYS_SELECT_EXPORT = "^+E"
CONTROL_TYPE_FILE_MENU = "MenuItem"
TITLE_FILE_MENU = "파일(F)"


def run_exports(lightroom: WindowSpecification, check_stop_flag):
    state_manager = StateManager()
    app_state = state_manager.get_state()

    if check_stop_flag("내보내기 시작 전 작업관리자 실행으로 자동화 중단"):
        return False

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

    if check_stop_flag("[내보내기 위치] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    else:
        export_location(
            export_window=export_window,
            app_state=app_state,
            check_stop_flag=check_stop_flag,
        )

    if check_stop_flag(
        "[파일이름 지정하기기] 자동화화 전 작업관리자 실행으로 자동화 중단"
    ):
        return False
    else:
        specs_filename(export_window=export_window, check_stop_flag=check_stop_flag)

    if check_stop_flag("[비디오] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    else:
        # 내보내기에 필요한 메뉴 아니지만,
        # 자동화 시야를 가리기 때문에 메뉴 닫음.
        collapse_video_opt(export_window=export_window, check_stop_flag=check_stop_flag)

    if check_stop_flag("[파일 설정] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    else:
        set_file(export_window=export_window, check_stop_flag=check_stop_flag)

    if check_stop_flag(
        "[collapse_credentials] 자동화 전 작업관리자 실행으로 자동화 중단"
    ):
        return False
    else:
        # 내보내기에 필요한 메뉴 아니지만,
        # 자동화 시야를 가리기 때문에 메뉴 닫음.
        collapse_credentials_opt(export_window=export_window, check_stop_flag=check_stop_flag)

    if check_stop_flag("[이미지 크기 조정] 자동화 전 작업관리자 실행으로 자동화 중단"):
        return False
    else:
        img_size_adjust(export_window=export_window, check_stop_flag=check_stop_flag)

    if check_stop_flag(
        "[내보내기 버튼 클릭] 자동화 전 작업관리자 실행으로 자동화 중단"
    ):
        return False
    else:
        export_button = export_window.child_window(
            title="내보내기", auto_id="1", control_type="Button"
        )

        export_button.click_input()

    use_identified_name_save = select_ui(
        win_specs=lightroom,
        title="고유한 이름 사용",
        control_type="Button",
        found_index=0,
    )

    is_identi_name_active = use_identified_name_save.exists()
    if is_identi_name_active == True:
        use_identified_name_save.click()
