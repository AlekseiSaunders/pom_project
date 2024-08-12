import os
from .utils import logger
from traceback import print_stack
from typing import Optional, List
from utilities.element_locator import ElementLocator
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import datetime



class ElementInteractor:
    """A class for interacting with web elements."""
    
    def __init__(self, driver):
        self.driver = driver
        self.locator = ElementLocator(driver)

    @staticmethod
    def scroll_to_element(driver: WebDriver, element: WebElement, timeout: int = 10) -> Optional[WebElement]:
        """
        Scroll to an element and wait for it to be visible.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            element (WebElement): The element to scroll to.
            timeout (int, optional): Maximum time to wait for the element. Defaults to 10.

        Returns:
            Optional[WebElement]: The visible element, or None if not visible.
        """
        try:
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()

            WebDriverWait(driver, timeout).until(EC.visibility_of(element))
            logger.info(f"Scrolled to {element} and it's visible")
            return element
        except TimeoutException:
            logger.error(f"Element not visible after scrolling within {timeout} seconds")
            return None

    @staticmethod
    def upload_file(file_input: WebElement, file_path: str) -> None:
        """
        Upload a file using a file input element.

        Args:
            file_input (WebElement): The file input element.
            file_path (str): Path to the file to be uploaded.
        """
        try:
            abs_file_path = os.path.abspath(file_path)
            file_input.send_keys(abs_file_path)
            logger.info(f"File uploaded: {abs_file_path}")
        except Exception as e:
            logger.warning(f"Could upload {file_input} found at {file_path}")
            logger.error(f"Error: {str(e)}")

    def element_click(self, locator, locator_type="XPATH"):
        """
        Click on an element

        Args:
            locator (_type_): _description_
        """
        
        try:
            element = self.locator.get_element(self.driver, locator, locator_type)
            element.click()
            logger.info(f"Element clicked successfully: {element.text}")
        except Exception as e:
            logger.warning(f"Could not click {locator} with {locator_type}")
            logger.error(f"Error: {str(e)}")
            
    def element_send_input(self, data, locator, locator_type="XPATH"):
        """
        Sends text to an element

        Args:
            locator (str): The locator, element, variable
            locator_type (str, optional): The method to find the element. Defaults to "XPATH".
        """
        try:
            element = self.locator.get_element(self.driver, locator, locator_type)
            element.send_keys(data)
        except Exception as e:
            logger.warning(f"Could send data into {locator}.")
            logger.error(f"Error: {str(e)}")
            