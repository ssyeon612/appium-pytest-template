from appium.webdriver.common.appiumby import AppiumBy

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        # 아이디 입력
        self.driver.find_element(AppiumBy.IOS_PREDICATE, 'value == "아이디 입력"').send_keys(username)

    def enter_password(self, password):
        # 비밀번호 입력
        self.driver.find_element(AppiumBy.IOS_PREDICATE, 'value == "비밀번호 입력"').send_keys(password)

    def tap_login_button(self):
        # 로그인 버튼 클릭
        self.driver.find_element(AppiumBy.IOS_PREDICATE, 
                                 'label == "로그인 하기" AND name == "로그인 하기" AND type == "XCUIElementTypeButton"').click()

    def is_logged_in(self):
        # 로그인 성공 여부 확인
        return self.driver.find_element_by_accessibility_id("homeScreen").is_displayed()
