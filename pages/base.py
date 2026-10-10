from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class Base:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get("https://www.saucedemo.com/")

    def click(self, locator, retries=3):
        for i in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    element
                )
                element.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if i == retries - 1:
                    raise
    
    def input(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def is_present(self, locator, timeout=1):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_visible(self, locator, timeout=1):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)