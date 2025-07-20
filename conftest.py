import pytest
from appium import webdriver

@pytest.fixture(scope="function")
def driver():
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",
        "app": "/path/to/your/app.apk",  # 실제 APK 경로로 바꿔야 함
        "automationName": "UiAutomator2"
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    yield driver
    driver.quit()
