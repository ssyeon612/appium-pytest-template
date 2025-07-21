import time

def test_login_success(driver):
    # 필요한 Page Object 불러오기
    from pages.mypage import MyPage
    from pages.login_method_select_page import LoginMethodSelectPage
    from pages.login_page import LoginPage

    # 페이지 객체 생성
    my_page = MyPage(driver)
    login_method_page = LoginMethodSelectPage(driver)
    login_page = LoginPage(driver)

    # 마이페이지 이동
    my_page.go_to_mypage()

    # 로그인/회원가입하기 클릭
    login_method_page.click_login_or_signup()

    # 로그인 방법 선택 (아이디 또는 다른 방법 → 아이디로 로그인)
    login_method_page.click_login_with_id_or_other()
    login_method_page.click_login_with_id()

    # 아이디와 비밀번호 입력 후 로그인
    login_page.enter_username("sytest04")
    login_page.enter_password("qwer1234!")
    login_page.tap_login_button()

    # 로그인 성공 여부 확인
    time.sleep(2)

    # 홈 화면 타이틀 존재 여부로 호그인 성공 판별
    assert login_page.is_logged_in()