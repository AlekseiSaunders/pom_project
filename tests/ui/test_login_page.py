import os
import pytest
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
        self.driver = setup_webdriver('chrome')
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        self.driver.get("https://www.letskodeit.com/")
    
        lp = LoginPage(self.driver)
        lp.login(admin_user, admin_pass)
        
        try:
            self.wait.until(EC.title_is('My Courses'))
            print("Login Successful")
        except:
            print("Login Failed")
            
    def test_all_elements(self):
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