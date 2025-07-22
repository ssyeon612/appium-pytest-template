from appium.webdriver.common.appiumby import AppiumBy

class LoginMethodSelectPage:
    def __init__(self, driver):
        self.driver = driver
        self.platform = driver.capabilities.get("platformName", "").lower()

    def click_login_or_signup(self):
        # '로그인/회원가입하기' 클릭
        print("self.platform:", self.platform)
        if self.platform == 'android':
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("로그인 / 회원가입하기")')
        else:
            locator = (AppiumBy.ACCESSIBILITY_ID, '로그인 / 회원가입하기')

        print("locator:", locator)
        self.driver.find_element(*locator).click()

    def click_login_with_id_or_other(self):
        # '아이디 또는 다른 방법으로 로그인' 클릭
        if self.platform == 'android':
            locator = (AppiumBy.ID, 'godticket.mobile:id/other_providers')
        else:
            locator = (AppiumBy.IOS_PREDICATE, 'label == "아이디 또는 다른 방법으로 로그인"')

        self.driver.find_element(*locator).click()

    def click_login_with_id(self):
        # '아이디로 로그인' 클릭
        if self.platform == 'android':
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("godticket.mobile:id/btn_system")')
        else:
            locator = (AppiumBy.ACCESSIBILITY_ID, '아이디로 로그인')

        self.driver.find_element(*locator).click()