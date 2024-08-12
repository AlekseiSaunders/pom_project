import os
import pytest
from faker import Faker
from utilities.utils import logger
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.login_page import LoginPage
from utilities.webdriver_setup import setup_webdriver
from utilities.config import DEFAULT_TIMEOUT, EXTENDED_TIMEOUT

# Initialize Faker
fake = Faker()

# Get env variables
load_dotenv()
admin_user = os.getenv("ADMIN_USERNAME")
admin_pass = os.getenv("ADMIN_PASSWORD")
fail_user = fake.email()
fail_pass = fake.password()
class TestLogin:
    
    @pytest.mark.run(order=1)
    @pytest.mark.fails
    def test_invalid_login(self):
        logger.info("Initializing driver and maximizing window")
        self.driver = setup_webdriver('chrome')
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.driver.get("https://www.letskodeit.com/")
        
        lp = LoginPage(self.driver)
        logger.info("Attempting to login from invalid test")
        lp.login(fail_user, fail_pass)
        login_failed = lp.verify_login_failed()
        assert login_failed, "Login was successful"
        
        
    @pytest.mark.run(order=2)
    @pytest.mark.succeeds
    def test_valid_login(self):
        logger.info("Initializing driver and maximizing window.")
        self.driver = setup_webdriver('chrome')
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.driver.get("https://www.letskodeit.com/")
    
        lp = LoginPage(self.driver)
        logger.info("Attempting to login from valid test")
        lp.login(admin_user, admin_pass)
        login_successful =  lp.verify_login_successful()
        assert login_successful, "Login was not successful"
    
            
    @pytest.mark.run(order=3)
    @pytest.mark.succeeds
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