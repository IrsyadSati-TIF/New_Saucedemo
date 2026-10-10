from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from .base import Base

class Cart(Base):
    def __init__(self, driver):
        super().__init__(driver)

        self.burger_btn = (By.ID, "react-burger-menu-btn")
        self.logout_btn = (By.ID, "logout_sidebar_link")
        self.cart_items = (By.CLASS_NAME, "cart_item")
        self.product_names = (By.CLASS_NAME, "inventory_item_name")
        self.product_prices = (By.CLASS_NAME, "inventory_item_price")
        self.product_quantity = (By.CLASS_NAME, "cart_quantity") 
        self.checkout_btn = (By.ID, "checkout")
        self.continue_shopping_btn = (By.ID, "continue-shopping")

    def logout(self):
        self.click(self.burger_btn)
        self.click(self.logout_btn)

    def is_it_cart_page(self):
        return "cart.html" in self.driver.current_url

    def get_product_list(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.cart_items))

    def get_product_names(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_names))
        return [element.text for element in elements]

    def get_product_prices(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_prices))
        return [element.text for element in elements]

    def get_product_name_price_qty(self):
        names = self.get_product_names()
        prices = self.get_product_prices()
        qty = self.get_product_quantity()

        return list(zip(names, prices, qty))

    def get_product_quantity(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_quantity))
        return [element.text for element in elements]

    def remove_product(self, product_name):
        products = self.wait.until(EC.presence_of_all_elements_located(self.cart_items))

        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text

            if name == product_name:
                button = product.find_element(By.CSS_SELECTOR, "button[id^='remove']")
                button.click()
                return

        raise Exception(f"Product '{product_name}' not found")

    def go_to_checkout_page(self):
        self.click(self.checkout_btn)

    def go_to_continue_shopping(self):
        self.click(self.continue_shopping_btn)

    def get_error_message(self):
        error_message = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text 
        return error_message
