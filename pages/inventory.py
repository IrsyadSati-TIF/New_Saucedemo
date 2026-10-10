from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from .base import Base

class Inventory(Base):
    def __init__(self, driver):
        super().__init__(driver)

        self.burger_btn = (By.ID, "react-burger-menu-btn")
        self.logout_btn = (By.ID, "logout_sidebar_link")
        self.product_items = (By.CLASS_NAME, "inventory_item")
        self.product_names = (By.CLASS_NAME, "inventory_item_name")
        self.product_prices = (By.CLASS_NAME, "inventory_item_price")
        self.dropdown_filter = (By.CLASS_NAME, "product_sort_container")
        self.add_to_cart_button = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        self.cart_button = (By.CLASS_NAME, "shopping_cart_link")

    def logout(self):
        self.click(self.burger_btn)
        self.click(self.logout_btn)

    def get_product_list(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.product_items))

    def get_product_names(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_names))
        return [element.text for element in elements]

    def get_product_prices(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_prices))
        return [element.text for element in elements]

    def get_product_name_price(self):
        names = self.get_product_names()
        prices = self.get_product_prices()

        return list(zip(names, prices))

    def filter_product(self, option):
        dropdown = self.wait.until(
            lambda driver: driver.find_element(*self.dropdown_filter)
        )

        select = Select(dropdown)
        select.select_by_visible_text(option)

    def add_product_to_cart(self, product_name):
        products = self.wait.until(EC.presence_of_all_elements_located(self.product_items))

        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text

            if name == product_name:
                button = product.find_element(*self.add_to_cart_button)
                button.click()
                return

        raise Exception(f"Product '{product_name}' not found")

    def remove_product(self, product_name):
        products = self.wait.until(EC.presence_of_all_elements_located(self.product_items))

        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text

            if name == product_name:
                button = product.find_element(By.CSS_SELECTOR, "button[id^='remove']")
                button.click()
                return

        raise Exception(f"Product '{product_name}' not found")

    def get_cart_count(self):
        elements = self.driver.find_elements(*self.cart_badge)

        if not elements:
            return 0

        return int(elements[0].text)

    def go_to_cart_page(self):
        self.click(self.cart_button)

    def get_error_message(self):
        error_message = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text 
        return error_message
