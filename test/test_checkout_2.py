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
from pages.checkout2 import Checkout2

class CheckoutTest_2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()

        # Wajib untuk CI/CD (Headless Mode)
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

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
        cls.checkout2_page = Checkout2(cls.driver)

    def setUp(self):
        self.base.load()
        self.login_page.login("standard_user", "secret_sauce")

    def test_1_verify_checkout_step_two_page(self):
        self.inventory_page.add_product_to_cart("Sauce Labs Backpack")
        self.inventory_page.add_product_to_cart("Sauce Labs Bike Light")
        self.inventory_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()
        self.checkout_page.input_data_pribadi()
        self.checkout_page.click_continue_checkout()

        print("="*50)
        print("### Verify Checkout Step Two Page ###")
        print("1. Start verifying")
        print("2. Is it checkout step two page?")
        result = self.checkout2_page.is_it_checkout_2_page()

        self.assertTrue(result, "User should be in checkout step two page")

        print("3. Result: ", result)
        print("4. Test complete")

    def test_2_verify_product_overview(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()
        self.checkout_page.input_data_pribadi()
        self.checkout_page.click_continue_checkout()

        print("="*50)
        print("### Verify Product Overview ###")
        print("1. Start verifying")
        expected = [
            ("Sauce Labs Backpack", "$29.99", "1"),
            ("Sauce Labs Bike Light", "$9.99", "1"),
            ("Sauce Labs Bolt T-Shirt", "$15.99", "1")
        ]

        print("2. Expected: ")
        for name, price, qty in expected:
            print(f"{name} - {price} : {qty}")

        actual = self.checkout2_page.get_product_name_price_qty()
        print("3. Actual: ")
        for name, price, qty in actual:
            print(f"{name} - {price} : {qty}")

        self.assertEqual(actual, expected, "Not Match")
        print("4. Complete")

    def test_3_verify_payment_shipping_information(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()
        self.checkout_page.input_data_pribadi()
        self.checkout_page.click_continue_checkout()

        print("="*50)
        print("### Verify Payment & Shipping Information ###")
        print("1. Start verifying")
        
        payment = self.checkout2_page.get_payment_information()
        shipping = self.checkout2_page.get_shipping_information()

        print("2. Payment: ", payment)
        print("3. shipping: ", shipping)

        self.assertEqual(payment, "SauceCard #31337", "Not Match")
        self.assertEqual(shipping, "Free Pony Express Delivery!", "Not Match")
        print("4. Complete")

    def test_4_verify_price_total(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()
        self.checkout_page.input_data_pribadi()
        self.checkout_page.click_continue_checkout()

        print("="*50)
        print("### Verify Price Total ###")
        print("1. Start verifying")
        item_total = self.checkout2_page.get_subtotal_price()
        tax = self.checkout2_page.get_tax_price()
        total = self.checkout2_page.get_total_price()

        print("2. ", item_total)
        print("3. ", tax)
        print("4. ", total)

        self.assertEqual(item_total, "Item total: $55.97", "Not Match")
        self.assertEqual(tax, "Tax: $4.48", "Not Match")
        self.assertEqual(total, "Total: $60.45", "Not Match")
        print("5. Complete")

    def test_5_finish_checkout(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()
        self.checkout_page.input_data_pribadi()
        self.checkout_page.click_continue_checkout()

        print("="*50)
        print("### Finish Checkout ###")
        print("1. Start click finish")
        self.checkout2_page.click_finish_checkout()
        
        print("2. Is it checkout complete page?")
        result = self.checkout2_page.is_it_checkout_complete_page()

        print("3. Result: ", result)
        self.assertTrue(result, "User not in checkout complete page")
        print("4. Test Complete")

    def test_6_cancel_checkout(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()
        self.checkout_page.input_data_pribadi()
        self.checkout_page.click_continue_checkout()

        print("="*50)
        print("### Cancel Checkout ###")
        print("1. Start click cancel")
        self.checkout_page.click_cancel_checkout()

        print("2. Is it inventory page?")
        result = self.login_page.is_logged_in()
        self.assertTrue(result, "User should be in inventory page")
        print("3. Result: ", result)
        print("4. Complete")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
if __name__ == "__main__":
    unittest.main()

