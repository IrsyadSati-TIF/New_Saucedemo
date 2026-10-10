import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from selenium import webdriver

from selenium.webdriver.common.by import By

from pages.base import Base
from pages.login import Login
from pages.inventory import Inventory
from pages.cart import Cart
from pages.checkout import Checkout

class CheckoutTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()

        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False
            }
        )

        cls.driver = webdriver.Chrome(options=options)
        cls.base = Base(cls.driver)
        cls.login_page = Login(cls.driver)
        cls.inventory_page = Inventory(cls.driver)
        cls.cart_page = Cart(cls.driver)
        cls.checkout_page = Checkout(cls.driver)

    def setUp(self):
        self.base.load()
        self.login_page.login("standard_user", "secret_sauce")

    def test_1_can_go_to_next_page(self):
        self.inventory_page.add_product_to_cart("Sauce Labs Backpack")
        self.inventory_page.add_product_to_cart("Sauce Labs Bike Light")
        self.inventory_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()

        print("="*50)
        print("### Can Go to Next Page ###")
        print("1. Start input mandatory fields")
        self.checkout_page.input_data_pribadi()

        print("2. Click continue")
        self.checkout_page.click_continue_checkout()

        print("3. Is it checkout-step-two?")
        result = self.checkout_page.is_it_checkout_2_page()
        self.assertTrue(result, "User should be in Cart Page")
        print("2. Result: ", result)
        print("3. Test complete")

    def test_2_first_name_blank(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()

        print("="*50)
        print("### First Name Blank ###")
        print("1. Start input last name & postal code")
        self.checkout_page.input_last_name()
        self.checkout_page.input_postal_code()

        print("2. Click continue")
        self.checkout_page.click_continue_checkout()

        print("3. Is it checkout step two?")
        result = self.checkout_page.is_it_checkout_2_page()
        error = self.checkout_page.get_error_message()
        self.assertFalse(result, "User should not in checkout step two")

        print("4. Result: ", result)
        print(error)
        print("6. Complete")

    def test_3_last_name_blank(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()

        print("="*50)
        print("### Last Name Blank ###")
        print("1. Start input first name & postal code")
        self.checkout_page.input_first_name()
        self.checkout_page.input_postal_code()

        print("2. Click continue")
        self.checkout_page.click_continue_checkout()

        print("3. Is it checkout step two?")
        result = self.checkout_page.is_it_checkout_2_page()
        error = self.checkout_page.get_error_message()
        self.assertFalse(result, "User should not in checkout step two")

        print("4. Result: ", result)
        print(error)
        print("6. Complete")

    def test_4_postal_code_blank(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()

        print("="*50)
        print("### Postal Code Blank ###")
        print("1. Start input first name & last name")
        self.checkout_page.input_first_name()
        self.checkout_page.input_last_name()

        print("2. Click continue")
        self.checkout_page.click_continue_checkout()

        print("3. Is it checkout step two?")
        result = self.checkout_page.is_it_checkout_2_page()
        error = self.checkout_page.get_error_message()
        self.assertFalse(result, "User should not in checkout step two")

        print("4. Result: ", result)
        print(error)
        print("6. Complete")

    def test_5_all_fields_blank(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()

        print("="*50)
        print("### All Fields Blank ###")
        print("1. Start click continue")
        self.checkout_page.click_continue_checkout()

        print("2. Is it checkout step two?")
        result = self.checkout_page.is_it_checkout_2_page()
        error = self.checkout_page.get_error_message()
        self.assertFalse(result, "User should not in checkout step two")

        print("3. Result: ", result)
        print(error)
        print("5. Complete")

    def test_6_go_to_prev_page(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()

        print("="*50)
        print("### Go to Prev Page ###")
        print("1. Start click cancel")
        self.checkout_page.click_cancel_checkout()

        print("2. Is it cart page?")
        result = self.cart_page.is_it_cart_page()
        self.assertTrue(result, "User should be in cart page")
        print("3. Result: ", result)
        print("4. Complete")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
if __name__ == "__main__":
    unittest.main()

