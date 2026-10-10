from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base import Base

class Login(Base):
    def __init__(self, driver):
        super().__init__(driver)

        self.username = (By.ID, "user-name")
        self.password = (By.ID, "password")
        self.login_btn = (By.ID, "login-button")
    
    def login(self, user, pwd):
        self.input(self.username, user)
        self.input(self.password, pwd)
        self.click(self.login_btn)

    def is_logged_in(self):
        return "inventory.html" in self.driver.current_url

    def is_logged_out(self):
        return (
            self.driver.current_url == "https://www.saucedemo.com/"
            and self.driver.find_element(
                *self.login_btn
            ).is_displayed()
        )

    def get_error_message(self):
        error_message = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text 
        return error_message
