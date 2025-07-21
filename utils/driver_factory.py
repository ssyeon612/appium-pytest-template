import json
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

def load_caps(platform: str):
    with open(f"drivers/{platform.lower()}_caps.json", "r") as f:
        return json.load(f)

def create_driver(platform="android"):
    caps = load_caps(platform)

    if platform.lower() == "android":
        options = UiAutomator2Options().load_capabilities(caps)
    elif platform.lower() == "ios":
        options = XCUITestOptions().load_capabilities(caps)
    else:
        raise ValueError(f"Unsupported platform: {platform}")

    return webdriver.Remote("http://localhost:4723", options=options)
