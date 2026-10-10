from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from .base import Base

class Checkout2(Base):
    def __init__(self, driver):
        super().__init__(driver)
        
        self.burger_btn = (By.ID, "react-burger-menu-btn")
        self.logout_btn = (By.ID, "logout_sidebar_link")

        #Checkout step 2
        self.cart_items = (By.CLASS_NAME, "cart_item")
        self.product_names = (By.CLASS_NAME, "inventory_item_name")
        self.product_prices = (By.CLASS_NAME, "inventory_item_price")
        self.product_quantity = (By.CLASS_NAME, "cart_quantity")
        self.payment_information = (By.CSS_SELECTOR, "[data-test='payment-info-value']")
        self.shipping_information = (By.CSS_SELECTOR, "[data-test='shipping-info-value']")
        self.subtotal_price = (By.CLASS_NAME, "summary_subtotal_label")
        self.tax_price = (By.CLASS_NAME, "summary_tax_label")
        self.total_price = (By.CLASS_NAME, "summary_total_label")

        #Navigation
        self.continue_checkout = (By.ID, "continue")
        self.cancel_checkout = (By.ID, "cancel")
        self.finish = (By.ID, "finish")

    def logout(self):
        self.click(self.burger_btn)
        self.click(self.logout_btn)

    def is_it_checkout_1_page(self):
        return "checkout-step-one.html" in self.driver.current_url

    def is_it_checkout_2_page(self):
        return "checkout-step-two.html" in self.driver.current_url

    def is_it_checkout_complete_page(self):
        return "checkout-complete.html" in self.driver.current_url

    def click_finish_checkout(self):
        self.click(self.finish)

    def click_cancel_checkout(self):
        self.click(self.cancel_checkout)

    def get_product_list(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.cart_items))

    def get_product_names(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_names))
        return [element.text for element in elements]

    def get_product_prices(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_prices))
        return [element.text for element in elements]

    def get_product_quantity(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_quantity))
        return [element.text for element in elements]

    def get_payment_information(self):
        element = self.wait.until(EC.presence_of_element_located(self.payment_information))
        return element.text

    def get_shipping_information(self):
        element = self.wait.until(EC.presence_of_element_located(self.shipping_information))
        return element.text

    def get_subtotal_price(self):
        element = self.wait.until(EC.presence_of_element_located(self.subtotal_price))
        return element.text

    def get_tax_price(self):
        element = self.wait.until(EC.presence_of_element_located(self.tax_price))
        return element.text

    def get_total_price(self):
        element = self.wait.until(EC.presence_of_element_located(self.total_price))
        return element.text

    def get_product_name_price_qty(self):
        names = self.get_product_names()
        prices = self.get_product_prices()
        qty = self.get_product_quantity()

        return list(zip(names, prices, qty))

    def get_error_message(self):
        error_message = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text 
        return error_message
