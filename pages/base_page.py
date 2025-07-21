from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10) # 기본 대기시간 10초

    def wait_for_element(self, locator_type, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator_type, locator)
        )
    
    def click_element(self, locator_type, locator):
        self.wait_for_element(locator_type, locator).click()

    def send_keys_to_element(self, locator_type, locator, text):
        self.wait_for_element(locator_type, locator).send_keys(text)