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



def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Specify the browser: chrome, firefox, edge or all",
    )
    parser.addoption(
        "--setup-type", 
        action="store",
        default="isolated",
        help="Specify the session type: isolated or continuous"
        )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--private",
        action="store_true",
        help="Run browser in private/incognito mode"
        )

@pytest.fixture(params=["chrome", "firefox", "edge"])
def all_browsers(request):
    return request.param


@pytest.fixture(scope="class")
def browser(request):
    browser_option = request.config.getoption("--browser")
    if browser_option == "all":
        return ["chrome", "firefox", "edge"]
    return [browser_option]

def perform_setup(browser_name, headless, private):
    logger.info(f"Setting up {browser_name} browser")
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.add_argument("--private")
        driver = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.add_argument("--inprivate")
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser request: {browser_name}")
    
    driver.maximize_window()
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    
    # Clear cookies and cache
    # driver.delete_all_cookies()
    # driver.execute_script("localStorage.clear();")
    # driver.execute_script("sessionStorage.clear();")
    
    start_test_capture(driver.session_id)
    
    return driver, wait

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
    
