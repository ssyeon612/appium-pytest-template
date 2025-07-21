from appium.webdriver.common.appiumby import AppiumBy

class LoginMethodSelectPage:
    def __init__(self, driver):
        self.driver = driver

    def click_login_or_signup(self):
        # '로그인/회원가입하기' 클릭
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인 / 회원가입하기').click()

    def click_login_with_id_or_other(self):
        # '아이디 또는 다른 방법으로 로그인' 클릭
        self.driver.find_element(AppiumBy.IOS_PREDICATE, 'label == "아이디 또는 다른 방법으로 로그인"').click()

    def click_login_with_id(self):
        # '아이디로 로그인' 클릭
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, '아이디로 로그인').click()
