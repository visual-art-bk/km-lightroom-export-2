from pywinauto import WindowSpecification


def check_title(export_window: WindowSpecification, main_title):
    print(f"모든 자식 타이틀 찾기 시작")

    children_texts = export_window.wrapper_object().children_texts()

    searched_title = None
    for text in children_texts:
        print(f"자식 타이틀 체크: {text}")
        print(f"메인 타이틀: {main_title}")

        if text == main_title:
            searched_title = main_title
            print(f"---> 메인 타이틀 찾았음: {main_title}")

    return searched_title
