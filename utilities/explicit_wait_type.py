from traceback import print_stack
from .utils import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from utilities.element_locator import ElementLocator


class ExplicitWaitType:

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, locator_type="xpath", timeout=10, poll_frequency=0.5):
        element = None
        locator = ElementLocator
        try:
            self.driver.implicitly_wait(0)
            by_type = self.locator.get_by_type(locator_type)
            logger.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout, poll_frequency, ignored_exceptions=[NoSuchElementException,
                                                                                               ElementNotVisibleException,
                                                                                               ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((by_type, locator)))
            logger.info("Element appeared on webpage")
        except Exception as e:
            logger.error(f"Element has not appeared on webpage: {str()}")
        self.driver.implicitly_wait(10)
        return element
