from pywinauto import WindowSpecification
from lightroom.utils.select_ui import select_ui
from lightroom.utils.check_title import check_title


def check_main_menu(export_window: WindowSpecification, main_title):
    print(f"------------------ {main_title} 자동화 시작 --------------------")

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

        export_opt_of_window.click_input()

        new_collapsible_selection = select_ui(
            title="Collapsible Section",
            control_type="Pane",
            found_index=0,
            win_specs=export_window,
        )

        return {"col": new_collapsible_selection, "main_menu": export_opt_of_window}

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
        print(f"[{main_title}] 요소 열려 있음 자동화 진행 시작.")
        return {"col": collapsible_selection, "main_menu": export_opt_of_window}

    print(f"[{main_title}] 요소 닫혀 있음 클릭해서 활성화")

    export_opt_of_window.click_input()

    new_collapsible_selection = select_ui(
        title="Collapsible Section",
        control_type="Pane",
        found_index=0,
        win_specs=export_window,
    )

    return {"col": new_collapsible_selection, "main_menu": export_opt_of_window}
