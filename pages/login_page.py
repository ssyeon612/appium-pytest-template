from appium.webdriver.common.appiumby import AppiumBy

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.platform = driver.capabilities.get("platformName", "").lower()

    def enter_username(self, username):
        # 아이디 입력
        if self.platform == 'android':
            locator = (AppiumBy.ID, 'godticket.mobile:id/et_id')
        else:
            locator = (AppiumBy.IOS_PREDICATE, 'value == "아이디 입력"')

        self.driver.find_element(*locator).send_keys(username)

    def enter_password(self, password):
        # 비밀번호 입력
        if self.platform == 'android':
            locator = (AppiumBy.ID, 'godticket.mobile:id/et_pw')
        else:
            locator = (AppiumBy.IOS_PREDICATE, 'value == "비밀번호 입력"')

        self.driver.find_element(*locator).send_keys(password)

    def tap_login_button(self):
        # 로그인 버튼 클릭
        if self.platform == 'android':
            locator = (AppiumBy.ID, 'godticket.mobile:id/bt_login')
        else:
            locator =  (AppiumBy.IOS_PREDICATE, 'label == "로그인 하기" AND name == "로그인 하기" AND type == "XCUIElementTypeButton"')
        
        self.driver.find_element(*locator).click()

    def is_logged_in(self):
        # 로그인 성공 여부 확인
        if self.platform == 'android':
            try:
                nick_element = self.driver.find_element(AppiumBy.ID, 'godticket.mobile:id/tv_nick_unit')
                return "님, 반가워요" in nick_element.text
            except Exception:
                return False
        else:
            return self.driver.find_elemnet(AppiumBy.ACCESSIBILITY_ID, 'homeScreen').is_displayed()
