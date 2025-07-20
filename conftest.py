import pytest
from utils.driver_factory import create_driver

def pytest_addoption(parser):
    parser.addoption(
        "--platform", action="store", default="android", help="Platform to test on: android or ios"
    )

@pytest.fixture(scope="function")
def driver(request):
    platform = request.config.getoption("--platform")
    driver = create_driver(platform)
    yield driver
    driver.quit()
