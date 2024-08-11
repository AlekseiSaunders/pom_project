# File: utilities/webdriver_setup.py

from selenium import webdriver
from .utils import logger
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import WebDriverException
from .config import CHROME_DRIVER_PATH, FIREFOX_DRIVER_PATH, EDGE_DRIVER_PATH


def setup_webdriver(browser_name='chrome', headless=False, private=False, driver_path=None):
    """
    Set up and return a WebDriver instance for the specified browser.

    :param browser_name: (str): Name of the browser ('chrome', 'firefox', or 'edge'). Default is 'chrome'.
    :param headless: (bool): Whether to run the browser in headless mode. Default is False.
    :param private: (bool): Whether to run the browser in private/incognito mode. Default is False.
    :param driver_path: (str): Optional path to the WebDriver executable. If None, Selenium will manage it automatically.
    :return: WebDriver: An instance of the specified WebDriver.
    """
    browser_name = browser_name.lower()

    if browser_name == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.add_argument("--incognito")
        service = ChromeService(executable_path=driver_path) if driver_path else ChromeService()
        driver_class = webdriver.Chrome
    elif browser_name == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.set_preference("browser.privatebrowsing.autostart", True)
        service = FirefoxService(executable_path=driver_path) if driver_path else FirefoxService()
        driver_class = webdriver.Firefox
    elif browser_name == 'edge':
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        if private:
            options.add_argument("--inprivate")
        service = EdgeService(executable_path=driver_path) if driver_path else EdgeService()
        driver_class = webdriver.Edge
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # Common options for stability and performance
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = driver_class(service=service, options=options)
        logger.info(f"{browser_name.capitalize()} WebDriver successfully initialized")
        if driver_path:
            logger.info(f"Using WebDriver at: {driver_path}")
        else:
            logger.info("Using Selenium-managed WebDriver")
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to initialize {browser_name.capitalize()} WebDriver: {str(e)}")
        raise
