import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

def create_driver(platform="android"):
    if platform.lower() == "android":
        desired_caps = {
            "platformName": "Android",
            "deviceName": "Android Emulator",
            "app": "/absolute/path/to/your-app.apk",  # 실제 경로로 수정
            "automationName": "UiAutomator2"
        }
    elif platform.lower() == "ios":
        desired_caps = {
            "platformName": "iOS",
            "platformVersion": "16.0",  # 버전에 맞게
            "deviceName": "iPhone Simulator",
            "app": "/absolute/path/to/your-app.app",
            "automationName": "XCUITest"
        }
    else:
        raise ValueError(f"Unsupported platform: {platform}")

    return webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
