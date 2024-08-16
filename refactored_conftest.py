import os
import pytest
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from utilities.utils import logger, start_test_capture, end_test_capture, get_logs_for_test
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT
from page_objects.login_page import LoginPage


"""
@package base
WebDriver factory class implementation
Creates a webdriver instance based on browser configurations.
Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""


load_dotenv()
BASE_URL = os.getenv("QA_BASE_URL")

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


class WebDriverFactory:
    
    def __init__(self, browser, headless=False, private=False):
        self.browser = browser
        self.headless = headless
        self.private = private

        
def get_webdriver_instance(self):
    if self.browser == "edge":
        options = EdgeOptions()
        if self.headless:
            options.add_argument("--headless")
        if self.private:
            options.add_argument("--inprivate")
        driver = webdriver.Edge(options=options)
    elif self.browser == 'chrome':
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        if self.private:
            options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
    elif self.browser == 'firefox':
        options = FirefoxOptions()
        if self.headless:
            options.add_argument("--headless")
        if self.private:
            options.add_argument("--private")
        driver = webdriver.Firefox(options=options)
    else:
        logger.error(f"Browser not recognized; {self.browser}")
    driver.maximize_window()
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    
    start_test_capture(driver.session_id)
    
    driver.get(BASE_URL)
    return driver, wait