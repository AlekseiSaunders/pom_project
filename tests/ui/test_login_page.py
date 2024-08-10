from selenium import webdriver



class LoginTests:
    
    def test_valid_login(self):
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.implicitly_wait(3)
        driver.get("https://www.letskodeit.com/")
    

        
        