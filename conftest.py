import os
import pytest
from datetime import datetime
from selenium import webdriver
from utilities.utils import logger
from utilities.utils import start_test_capture, end_test_capture, get_logs_for_test


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Specify the browser: chrome, firefox, edge or all",
    )


@pytest.fixture(scope="class")
def browser(request):
    browser_option = request.config.getoption("--browser")
    if browser_option == "all":
        return ["chrome", "firefox", "edge"]
    return [browser_option]


@pytest.fixture()
def setup_teardown(request, browser):
    drivers = []
    for browser_name in browser:
        if browser_name == "chrome":
            drivers.append(webdriver.Chrome())
        elif browser_name == "firefox":
            drivers.append(webdriver.Firefox())
        elif browser_name == "edge":
            drivers.append(webdriver.Edge())
        else:
            raise ValueError(f"Unsupported browser request: {browser}")
    for driver in drivers:
        driver.maximize_window()
    print("This is setting something up, once before each method in case1")

    yield drivers[0] if len(drivers) == 1 else drivers

    print("This runs after each test. Tear Down 1")
    for driver in drivers:
        driver.close()


@pytest.fixture(scope="class")
def one_time_setup(request, browser):
    print("Running one time setup")
    if browser == "firefox":
        value = 10
        print("Running tests on Firefox, value = 10")
    elif browser == "chrome":
        value = 20
        print("Running tests on Chrome, value = 20")
    else:
        value = 10
        print("Value is 30")

    if request.cls is not None:
        request.cls.value = value

    yield value

    print("Running one time tear down")


@pytest.fixture(params=["chrome", "firefox", "edge"])
def all_browsers(request):
    return request.param


def pytest_configure(config):
    # Get the test suite name
    suite_name = "pytestpackage"

    if not os.path.isdir(os.path.join(config.rootdir, suite_name)):
        suite_name = os.path.basename(config.rootdir)

    # Get current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Contruct the report name
    report_name = f"{suite_name}_{timestamp}_report.html"
    
    reports_dir = os.path.join(config.rootdir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    report_path = os.path.join(reports_dir, report_name)

    # Find the --html option in the config
    # html_path = None
    # for arg in config.option.htmlpath:
    #     if arg.endswith('.html'):
    #         html_path = arg
    #         break

    # if html_path:
    #     # Replace original html path with our custom name
    #     config.option.htmlpath = [
    #         report_name if arg == html_path else arg for arg in config.option.htmlpath
    #     ]

    if config.option.htmlpath:
        config.option.htmlpath = report_path


def pytest_html_report_title(report):
    datestamp = datetime.now().strftime("%A - %m%Y")
    timestamp = datetime.now().strftime("%H:%M:%S")
    report.title = f"Testing WildXR Website - on {datestamp} @ {timestamp}"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == call:
        # Captures logs for the test.
        logs = get_logs_for_test(item.name)
        
        # Adds logs to the report.
        extra = getattr(report, 'extra', [])
        extra.append(pytest.html.extras.text(logs, name="Log"))
        report.extra = extra
        
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    # Clear the log capture for this test
    start_test_capture(item.name)
    yield
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_teardown(item):
    end_test_capture(item.name)
    yield