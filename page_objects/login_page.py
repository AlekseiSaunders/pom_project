import os
import time
from utilities.utils import logger
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.element_locator import ElementLocator
from utilities.element_interactor import ElementInteractor
from utilities.config import DEFAULT_TIMEOUT


load_dotenv()

class LoginPage:
    """
    Page Object for login page
    This class contains methods to interact with the login page element
    """
    
    def __init__(self, driver):
        """
        Initialize the LoginPage object.

        Args:
            driver (webdriver): The Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.locator = ElementLocator(driver)
        self.interact = ElementInteractor(driver)
        
    # Locators
    _login_link = "//div[contains(@class, 'navbar')]//a[@href='/login']"
    _username_input = "//form[contains(@method, 'POST')]//input[@type='email']"
    _password_input = "//form[contains(@method, 'POST')]//input[@type='password']"
    _login_button = "//form[contains(@method, 'POST')]//button[@id='login']"
    _dropdown_menu = "//button[@id='dropdownMenu1']"
        
    
    def click_login_link(self):
        """Click the login link."""
        logger.info("Clicking login link from click_method.")
        self.interact.element_click(self._login_link)
        
    def enter_username(self, user):
        """
        Enter the username into the username input field.

        Args:
            username (str): The username for the test account.
        """
        logger.info("Entering user: {user}.")
        self.interact.element_send_input(user, self._username_input)
        
    def enter_password(self, password):
        """
        Enter the password into the password input field.

        Args:
            password (str): The password for the associated username.
        """
        logger.info("Entering password.")
        self.interact.element_send_input(password, self._password_input)
        
    def click_login_button(self):
        """Click the login button"""
        logger.info("Clicking the login button.")
        self.interact.element_click(self._login_button)
        
    def verify_all_elements_present(self):
        """
        Verify that all required elements are present of the page
        
        Returns: 
            bool: True is all elements are present, False otherwise
        """
        logger.info("Attempting to click login link from verify_method")
        self.click_login_link()
        
        logger.info("Verifying all expected elements are present.")
        try:
            for locator in [self._login_button, self._username_input, self._password_input]:
                self.wait.until(EC.presence_of_element_located((By.XPATH, locator)))
                logger.info(f"{locator} was located succesfully.")
            return True
        except NoSuchElementException:
            logger.error(f"Could not find {locator}")
            return False
        
    def login(self, user, password):
        """
        Performs the login action.

        Args:
            username (str): The username to log in with
            password (str): The password to log in with
            
        Raises:
            TimeoutException: If the login process take to long or fails.
        """
        logger.info(f"Attempting login for user: {user}")
        self.click_login_link()
        self.enter_username(user)
        self.enter_password(password)
        self.click_login_button()
        
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self._dropdown_menu)))
            logger.info(f"Login successful, user account dropdown found")
        except TimeoutException:
            logger.error("Login failed or took too long to complete.")
            raise TimeoutException("Login failed or took too long to complete.")
        
    