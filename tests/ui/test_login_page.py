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
admin_user = os.getenv("USERNAME")
admin_pass = os.getenv("USERPASSWORD")



class TestLogin:
    
    def test_valid_login(self):
        driver = setup_webdriver('chrome')
        driver.maximize_window()
        driver.implicitly_wait(DEFAULT_TIMEOUT)
        driver.get("https://www.letskodeit.com/")
    
        lp = LoginPage(driver)
        lp.login(admin_user, admin_pass)
        
        
        page_title = driver.find_element(By.XPATH, "//title")
        title_name = page_title.get_attribute('innerHTML')
        expected_title = 'My Courses'
        print(title_name)
        if title_name == expected_title:
            print("Login Successful")
        else:
            print("Login Failed")
        
        
TL = TestLogin()
TL.test_valid_login()