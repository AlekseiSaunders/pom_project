import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from utilities.utils import logger, start_test_capture, end_test_capture, get_logs_for_test
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT
from page_objects.login_page import LoginPage
from refactored_conftest import WebDriverFactory

def perform_setup(browser_name, headless, private):
    logger.info(f"Setting up {browser_name} browser")
    wdf = WebDriverFactory(browser_name, headless, private)
    driver = wdf.get_webdriver_instance()
    yield driver
    
@pytest.fixture(scope="function")
def setup(request):
    setup_type = request.config.getoption("--setup-type")
    
    if setup_type == "isolated":
        yield from setup_isolated(request)
    elif setup_type == "continuous":
        yield from setup_continuous(request)
    else:
        raise ValueError(f"Invalid setup type: {setup_type}")

@pytest.fixture(scope="function")
def setup_isolated(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    private = request.config.getoption("--private")
    
    drivers = []
    for browser_name in (browser if isinstance(browser, list) else [browser]):
        driver, wait = perform_setup(browser_name, headless, private)
        drivers.append((driver, wait))
    
    logger.info("Setting up isolated test")
    driver, wait = drivers[0] if len(drivers) == 1 else drivers
    request.node.driver = driver # Attach driver to the test node for teardown
    
    yield driver, wait
    
    # Perform teardown 
    perform_teardown(driver)
    
@pytest.fixture(scope="class")
def setup_continuous(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    private = request.config.getoption("--private")
    
    drivers = []
    for browser_name in (browser if isinstance(browser, list) else [browser]):
        driver, wait = perform_setup(browser_name, headless, private)
        drivers.append((driver, wait))
    
    logger.info("Setting up continuous session for test")
    
    driver, wait = drivers[0] if len(drivers) == 1 else drivers
    request.cls.driver = driver
    request.cls.wait = wait
    yield driver, wait
    
    # Perform teardown
    perform_teardown(driver)
    

# def perform_teardown(driver):
#     logger.info("Performing teardown")
#     if isinstance(driver, list):
#         for d in driver:
#             teardown_single_driver(d)
#         else:
#             teardown_single_driver(driver)

def perform_teardown(driver):
    try:
        logger.info(f"Attempting teardown with perform_teardown")
    # Close the browser
        driver.quit()
        
    # Log out if logged in
    # try:
    #     login_page = LoginPage(driver)
    #     if login_page.is_logged_in():
    #         login_page.logout()
    # except Exception as e:
    #     logger.error(f"Error during logout str({e})")
    
    # Clear browsing data
    # driver.delete_all_cookies()
    # driver.execute_script("localStorage.clear();")
    # driver.exceute_script("sessionStorage.clear();")
    except Exception as e:
        logger.warning(f"Problem performing teardown steps: {str(e)}")
    
        
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
    
