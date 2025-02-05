from pywinauto import WindowSpecification
from pywinauto.controls.uia_controls import ComboBoxWrapper


def select_combobox(
    win_specs: WindowSpecification,
    title_combobox_label,
    control_type_combobox,
    context="콤보박스",
) -> ComboBoxWrapper:
    folder_label = win_specs.child_window(
        title=title_combobox_label, control_type=control_type_combobox
    )
    # folder_label = win_specs.child_window(title="폴더:", control_type="Text")

    parent_pane = folder_label.parent()

    # 부모 Pane에서 '내보낼 위치' ComboBox 찾기
    export_location_combo = None
    for element in parent_pane.descendants(control_type="ComboBox"):
        if element.rectangle().bottom < folder_label.rectangle().top:
            export_location_combo = element
            break  # 첫 번째 발견된 ComboBox 선택

    if not export_location_combo:
        print(f"{context} 를 찾을 수 없습니다.")
        return

    return export_location_combo
