import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.element_locator import ElementLocator
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
        self.locator = ElementLocator()
        
    # Locators
    _login_link = "//div[contains(@class, 'navbar')]//a[@href='/login']"
    _username_input = "//form[contains(@method, 'POST')]//input[@type='email']"
    _password_input = "//form[contains(@method, 'POST')]//input[@type='password']"
    _login_button = "//form[contains(@method, 'POST')]//button[@id='login']"
    _dropdown_menu = "//button[@id='dropdownMenu1']"
    
    def get_login_link(self):
        """Get the login link element."""
        return self.locator.get_element(self.driver, self._login_link)
    
    def get_username_input(self):
        """Get the username input element."""
        return self.locator.get_element(self.driver, self._username_input)
    
    def get_password_input(self):
        """Get the password input element."""
        return self.locator.get_element(self.driver, self._password_input)
    
    def get_login_button(self):
        """Get the login button element."""
        return self.locator.get_element(self.driver, self._login_button)
    
    def click_login_link(self):
        """Click the login link."""
        self.get_login_link().click()
        
    def enter_username(self, username):
        """
        Enter the username into the username input field.

        Args:
            username (str): The username for the test account.
        """
        self.get_username_input().send_keys(username)
        
    def enter_password(self, password):
        """
        Enter the password into the password input field.

        Args:
            password (str): The password for the associated username.
        """
        self.get_password_input().send_keys(password)
        
    def click_login_button(self):
        """Click the login button"""
        self.get_login_button().click()
        
    def verify_all_elements_present(self):
        """
        Verify that all required elements are present of the page
        
        Returns: 
            bool: True is all elements are present, False otherwise
        """
        try:
            self.get_username_input
            self.get_password_input
            self.get_login_button
            return True
        except NoSuchElementException:
            return False
        
    def login(self, username, password):
        """
        Performs the login action.

        Args:
            username (str): The username to log in with
            password (str): The password to log in with
            
        Raises:
            TimeoutException: If the login process take to long or fails.
        """
        
        self.click_login_link()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self._dropdown_menu)))
        except TimeoutException:
            raise TimeoutException("Login failed or took too long to complete.")
        
    