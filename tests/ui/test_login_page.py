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
from utilities.screenshot_manager import ScreenshotManager

# Initialize Faker
fake = Faker()

# Initialize ScreenshotManager
shot = ScreenshotManager()

# Get env variables
load_dotenv()
admin_user = os.getenv("ADMIN_USERNAME")
admin_pass = os.getenv("ADMIN_PASSWORD")
fail_user = fake.email()
fail_pass = fake.password()


class TestLogin:
    
    @pytest.mark.run(order=1)
    @pytest.mark.fails
    def test_invalid_login(self, setup_isolated):
        driver,wait = setup_isolated
        
        logger.info(f"Attempting to login from invalid test on {driver.name}")
        driver.get("https://www.letskodeit.com/")
        
        lp = LoginPage(driver)
        lp.login(fail_user, fail_pass)
        login_failed = lp.verify_login_failed()
        assert login_failed, "Login was successful"
        
        
    @pytest.mark.run(order=2)
    @pytest.mark.succeeds
    def test_valid_login(self, setup_isolated):
        driver, wait = setup_isolated
        logger.info(f"Attempting to login from valid test on {driver.name}")
        driver.get("https://www.letskodeit.com/")
    
        lp = LoginPage(driver)
        lp.login(admin_user, admin_pass)
        login_successful =  lp.verify_login_successful()
        assert login_successful, "Login was not successful"
    
            
    @pytest.mark.run(order=3)
    @pytest.mark.succeeds
    def test_all_elements(self, setup_isolated):
        driver, wait = setup_isolated

        logger.info(f"Verifying all elements are present on {driver.name}")
        driver.get("https://www.letskodeit.com/")

        lp = LoginPage(driver)
        lp.verify_all_elements_present()
            

if __name__ == "__main__":
    TL = TestLogin()
    TL.test_invalid_login()
    TL.test_valid_login()
    TL.test_all_elements()