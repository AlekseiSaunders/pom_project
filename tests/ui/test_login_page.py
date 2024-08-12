import os
import pytest
from utilities.utils import logger
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.login_page import LoginPage
from utilities.webdriver_setup import setup_webdriver
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT


load_dotenv()
admin_user = os.getenv("ADMIN_USERNAME")
admin_pass = os.getenv("ADMIN_PASSWORD")



class TestLogin:
    
    def test_valid_login(self):
        logger.info("Initializing driver and maximizing window.")
        self.driver = setup_webdriver('chrome')
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.driver.get("https://www.letskodeit.com/")
    
        lp = LoginPage(self.driver)
        logger.info("Attempting to login")
        lp.login(admin_user, admin_pass)
        
        try:
            self.wait.until(EC.title_is('My Courses'))
            logger.info("Login Successful")
        except Exception as e:
            logger.warning("Login Failed")
            logger.error(f"Error: {str(e)}")
            
    def test_all_elements(self):
        logger.info("Initializing driver and maximizing window.")
        self.driver = setup_webdriver('chrome')
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.driver.get("https://www.letskodeit.com/")
        
        lp = LoginPage(self.driver)
        lp.verify_all_elements_present()
            

if __name__ == "__main__":
    TL = TestLogin()
    TL.test_valid_login()
    TL.test_all_elements()