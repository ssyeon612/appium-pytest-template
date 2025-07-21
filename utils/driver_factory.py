import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

def create_driver(platform="android"):
    if platform.lower() == "android":
        desired_caps = {
            "platformName": "Android",
            "deviceName": "Android Emulator",
            "app": "/absolute/path/to/your-app.apk",
            "automationName": "UiAutomator2"
        }
        options = UiAutomator2Options().load_capabilities(desired_caps)
    elif platform.lower() == "ios":
        desired_caps = {
            "platformName": "iOS",
            "platformVersion": "16.0",
            "deviceName": "iPhone Simulator",
            "app": "/absolute/path/to/your-app.app",
            "automationName": "XCUITest"
        }
        options = XCUITestOptions().load_capabilities(desired_caps)
    else:
        raise ValueError(f"Unsupported platform: {platform}")

    return webdriver.Remote("http://localhost:4723", options=options)
