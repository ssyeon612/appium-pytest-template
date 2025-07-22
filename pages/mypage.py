from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MyPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_mypage(self):
        # 마이페이지 탭 클릭
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, '마이'))
        ).click()
