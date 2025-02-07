from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_export_option import check_export_option


def collapse_video_opt(export_window: WindowSpecification):

    (
        _,
        export_opt_of_col,
    ) = check_export_option(win_specs=export_window, export_opt_title="비디오")

    export_opt_of_window = select_ui(
        win_specs=export_window,
        control_type="Pane",
        title="비디오",
        found_index=0,
    )

    if export_opt_of_col == None:
        print("비디오 메뉴 이미 닫혀있음")

    else:
        export_opt_of_window.click_input()
        print("비디오 메뉴 닫았음")

    print("비디오 메뉴 초기화")
