import time

# @allure.epic("회원 기능")
# @allure.feature("로그인")
# @allure.story("정상 로그인")
# @allure.title("아이디 비밀번호 로그인 성공")
# @allure.description("정상적인 계정으로 로그인하여 홈화면 진입을 확인한다.")
def test_login_success(driver):
    # 필요한 Page Object 불러오기
    from pages.mypage import MyPage
    from pages.login_method_select_page import LoginMethodSelectPage
    from pages.login_page import LoginPage

    # 페이지 객체 생성
    my_page = MyPage(driver)
    login_method_page = LoginMethodSelectPage(driver)
    login_page = LoginPage(driver)

    # with allure.step("마이페이지로 이동"):
    my_page.go_to_mypage()

    # with allure.step("로그인 방법 선택"):
    #     login_method_page.click_login_or_signup()
    #     login_method_page.click_login_with_id_or_other()
    #     login_method_page.click_login_with_id()

    # with allure.step("아이디/비밀번호 입력"):
    #     login_page.enter_username("sytest04")
    #     login_page.enter_password("qwer1234!")
    #     login_page.tap_login_button()

    # with allure.step("로그인 성공 여부 확인"):
    #     time.sleep(2)
    #     assert login_page.is_logged_in()