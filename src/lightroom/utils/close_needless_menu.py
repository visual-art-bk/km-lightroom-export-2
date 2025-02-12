from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_title import check_title


def close_needless_menu(export_window: WindowSpecification, main_title):
    print(
        f"------------------ 자동화 대상 아닌 메뉴 - {main_title} 검사 시작 --------------------"
    )

    export_opt_of_window = select_ui(
        win_specs=export_window,
        title=main_title,
        control_type="Pane",
        found_index=0,
    )

    collapsible_menu = select_ui(
        title="Collapsible Section",
        control_type="Pane",
        found_index=0,
        win_specs=export_window,
    )

    is_exists_collapsible = collapsible_menu.exists()

    if is_exists_collapsible == False:
        print("모든 내보내기 메뉴 닫혀있음")
        print(f"---> 자동화 대상 아닌 메뉴 {main_title} 검사 완료")
        return

    print("특정되지 않은 메뉴가 열려 있음")

    collapsible_selection = select_ui(
        title="Collapsible Section",
        control_type="Pane",
        found_index=0,
        win_specs=export_window,
    )

    title_by_collapsible = check_title(
        export_window=collapsible_selection, main_title=main_title
    )

    if title_by_collapsible == main_title:
        print(f"자동화대상 아닌 [{main_title}] 요소 열려 있음 - 클릭해서 메뉴닫음.")
        export_opt_of_window.click_input()
        return

    print(f"자동화대상 아닌 [{main_title}] 요소 닫혀 있음 - 다음 자동화 진행")
    return
