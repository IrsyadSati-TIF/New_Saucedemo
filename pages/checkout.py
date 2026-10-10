from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from .base import Base

class Checkout(Base):
    def __init__(self, driver):
        super().__init__(driver)
        
        self.burger_btn = (By.ID, "react-burger-menu-btn")
        self.logout_btn = (By.ID, "logout_sidebar_link")

        #Checkout step 1
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.postal_code = (By.ID, "postal-code")

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
        self.finish = ()

    def logout(self):
        self.click(self.burger_btn)
        self.click(self.logout_btn)

    def is_it_checkout_1_page(self):
        return "checkout-step-one.html" in self.driver.current_url

    def is_it_checkout_2_page(self):
        return "checkout-step-two.html" in self.driver.current_url

    def click_continue_checkout(self):
        self.click(self.continue_checkout)

    def click_cancel_checkout(self):
        self.click(self.cancel_checkout)

    def input_data_pribadi(self):
        self.input(self.first_name, "Irsyad")
        self.input(self.last_name, "Sati")
        self.input(self.postal_code, "081960")

    def input_first_name(self):
        self.input(self.first_name, "Irsyad")

    def input_last_name(self):
        self.input(self.last_name, "Sati")

    def input_postal_code(self):
        self.input(self.postal_code, "081960")

    def get_product_list(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.cart_items))

    def get_product_names(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_names))
        return [element.text for element in elements]

    def get_product_prices(self):
        elements = self.wait.until(EC.presence_of_all_elements_located(self.product_prices))
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

    def get_error_message(self):
        error_message = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text 
        return error_message
