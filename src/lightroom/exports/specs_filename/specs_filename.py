from pywinauto import  WindowSpecification
from lightroom.utils.select_ui import select_ui



def set_filename(export_window: WindowSpecification):
    try:
        # 내보내기 위치 메뉴 찾고 클릭
        setting_filename = select_ui(
            win_specs=export_window, control_type="Pane", title="파일 이름 지정"
        )
        setting_filename.click_input()

    except Exception:
        print("파일 이름 지정이이 열려있음 다음으로 넘어갑니다.")

    collapsible_selection = select_ui(
        found_index=0,
        control_type="Pane",
        title="Collapsible Section",
        win_specs=export_window,
    )

    checkbox = select_ui(
        control_type="CheckBox",
        title="바꿀 이름:",
        win_specs=collapsible_selection,
    )
    # 현재 토글 대신
    checkbox.click_input()
    checkbox.click_input()

    combobox = collapsible_selection.child_window(
        control_type="ComboBox", found_index=0
    )
    combobox.select("사용자 정의 이름 - 시퀀스")

    edit_field = select_ui(
        control_type="Edit",
        title="사용자 정의 텍스트:",
        win_specs=collapsible_selection,
        found_index=0,
    )

    edit_field.set_text("")
    edit_field.set_text("필터")

    setting_filename.click_input()
