import time

def test_login_success(driver):
    from pages.login_page import LoginPage

    login_page = LoginPage(driver)

    login_page.enter_username("testuser")
    login_page.enter_password("testpassword")
    login_page.tap_login_button()

    time.sleep(2) # 필요시 대기

    assert login_page.is_logged_in()