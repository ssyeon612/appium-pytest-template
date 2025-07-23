import pytest, time, os
from utils.driver_factory import create_driver

def pytest_addoption(parser):
    parser.addoption(
        "--platform", action="store", default="android", help="Platform to test on: android or ios"
    )

@pytest.fixture(scope="function")
def driver(request):
    platform = request.config.getoption("--platform")
    try:
        driver = create_driver(platform)
    except Exception as e:
        print("Driver 생성 실패:", e)
        raise
    yield driver

    # === teardown: 실패 시 스크린샷 저장 ===
    if request.node.rep_call.failed:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        folder = "screenshots"
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"failure_{timestamp}.png")
        driver.save_screenshot(filename)
        print(f"[SCREENSHOT] 테스트 실패 - 스크린샷 저장됨: {filename}")

    driver.quit()

# === hook: 테스트 결과를 fixture에서 알 수 있게 해주는 코드 ===
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 각 테스트 단계 (setup/call/teardown) 결과 수집
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
