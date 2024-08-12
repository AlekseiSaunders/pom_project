# element_locator.py

import os
from .utils import logger
from typing import Optional, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import datetime


class ElementLocator:
    """A class for locating web elements."""
    
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def get_by_type(locator_type: str) -> Optional[str]:
        """
        Get the Selenium By type based on a string locator type.

        Args:
            locator_type (str): The type of locator (e.g., 'id', 'xpath', 'css').

        Returns:
            Optional[str]: The Selenium By type, or None if not supported.
        """
        locator_type = locator_type.lower()
        locator_map = {
            "id": By.ID,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "classname": By.CLASS_NAME,
            "linktext": By.LINK_TEXT,
            "name": By.NAME
        }
        if locator_type not in locator_map:
            logger.error(f"Locator type '{locator_type}' is not supported")
            return None
        return locator_map[locator_type]

    @staticmethod
    def get_element(driver: WebDriver, locator: str, locator_type: str = 'xpath') -> Optional[WebElement]:
        """
        Find a web element using the specified locator and locator type.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (str): The locator string.
            locator_type (str, optional): The type of locator. Defaults to 'xpath'.

        Returns:
            Optional[WebElement]: The found WebElement, or None if not found.
        """
        try:
            by_type = ElementLocator.get_by_type(locator_type)
            if by_type is None:
                return None
            element = driver.find_element(by_type, locator)
            logger.info(f"Element found with locator: {locator}")
            return element
        except NoSuchElementException:
            logger.error(f"Element not found with locator: {locator}")
            return None

    @staticmethod
    def is_element_present(driver: WebDriver, locator: str, locator_type: str = "xpath") -> bool:
        """
        Check if an element is present on the page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (str): The locator string.
            by_type (str, optional): The type of locator. Defaults to By.XPATH.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        try:
            driver.find_element(locator_type, locator)
            logger.info(f"Element found with locator: {locator}")
            return True
        except NoSuchElementException:
            logger.info(f"Element not found with locator: {locator}")
            return False

    @staticmethod
    def are_elements_present(driver: WebDriver, locator: str, locator_type: str = "xpath") -> bool:
        """
        Check if one or more elements are present on the page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (str): The locator string.
            by_type (str, optional): The type of locator. Defaults to By.XPATH.

        Returns:
            bool: True if one or more elements are present, False otherwise.
        """
        elements = driver.find_elements(locator_type, locator)
        if elements:
            logger.info(f"{len(elements)} element(s) found with locator: {locator}")
            return True
        else:
            logger.info(f"No elements found with locator: {locator}")
            return False
