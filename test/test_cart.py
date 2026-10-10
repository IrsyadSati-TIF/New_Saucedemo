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

class CartTest(unittest.TestCase):

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

    def setUp(self):
        self.base.load()
        self.login_page.login("standard_user", "secret_sauce")

    def test_1_verify_cart_page(self):
        self.inventory_page.add_product_to_cart("Sauce Labs Backpack")
        self.inventory_page.add_product_to_cart("Sauce Labs Bike Light")
        self.inventory_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
        self.inventory_page.go_to_cart_page()

        print("="*50)
        print("### Verify Cart Page ###")
        print("1. Start verifying")

        result = self.cart_page.is_it_cart_page()

        self.assertTrue(result, "User should be in Cart Page")

        print("2. Result: ", result)
        print("3. Test complete")

    def test_2_verify_product_in_cart(self):
        self.inventory_page.go_to_cart_page()

        print("="*50)
        print("### Verify Product In Cart ###")
        print("1. Start verifying")

        products = self.cart_page.get_product_list()

        print("2. Expected: 3")
        print("3. Actual: ", len(products))

        self.assertEqual(len(products), 3, "Cart should contain 3 products")
        
        print("4. Test Complete")

    def test_3_verify_product_name(self):
        self.inventory_page.go_to_cart_page()

        print("="*50)
        print("### Verify Product Name ###")
        print("1. Start Verifying")
        expected = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt"
        ]

        print("2. Expected product: ")
        for product in expected:
            print("-", product)

        actual = self.cart_page.get_product_names()

        print("3. Actual product: ")
        for product in actual:
            print("-", product)

        self.assertEqual(expected, actual, "Product names should match with expected product")
        print("4. Test complete")

    def test_4_verify_product_price(self):
        self.inventory_page.go_to_cart_page()

        print("="*50)
        print("### Verify Product Price ###")
        print("1. Start Verifying")
        expected = [
            "$29.99",
            "$9.99",
            "$15.99"
        ]

        print("2. Expected Price List: ")
        for price in expected:
            print("-", price)

        actual = self.cart_page.get_product_prices()

        print("3. Actual price list: ")
        for price in actual:
            print("-", price)

        self.assertEqual(actual, expected, "Price list should match with expected price")
        print("4. Test complete")

    def test_5_verify_product_quantity(self):
        self.inventory_page.go_to_cart_page()

        print("="*50)
        print("### Verify Product Quantity ###")
        print("1. Start Verifying")
        expected = [
            "1",
            "1",
            "1"
        ]

        print("2. Expected product quantity: ")
        for i in expected:
            print("-", i)

        actual = self.cart_page.get_product_quantity()

        print("3. Actual product quantity: ")
        for i in actual:
            print("-", i)

        self.assertEqual(expected, actual, "Quantity product should match with expected")
        print("4. Test complete")

    def test_6_verify_product_name_price_qty(self):
        self.inventory_page.go_to_cart_page()

        print("="*50)
        print("### Verify Product Name, Price, and Qty ###")
        print("1. Start Verifying")
        expected = [
            ("Sauce Labs Backpack", "$29.99", "1"),
            ("Sauce Labs Bike Light", "$9.99", "1"),
            ("Sauce Labs Bolt T-Shirt", "$15.99", "1")
        ]

        print("2. Expected :")
        for name, price, qty in expected:
            print(f"{name} - {price} - {qty}")

        actual = self.cart_page.get_product_name_price_qty()

        print("3. Actual: ")
        for name, price, qty in actual:
            print(f"{name} - {price} - {qty}")

        self.assertEqual(expected, actual, "Product list should match with expected")
        print("4. Test complete")

    def test_7_remove_from_cart(self):
        self.inventory_page.go_to_cart_page()

        print("="*50)
        print("### Remove From Cart ###")
        print("1. Start test")

        product = "Sauce Labs Backpack"

        self.cart_page.remove_product(product)

        expected = [
            ("Sauce Labs Bike Light", "$9.99", "1"),
            ("Sauce Labs Bolt T-Shirt", "$15.99", "1")
        ]

        print("2. Expected: ")
        for name, price, qty in expected:
            print(f"{name} - {price} - {qty}")

        actual = self.cart_page.get_product_name_price_qty()

        print("3. Actual: ")
        for name, price, qty in actual:
            print(f"{name} - {price} - {qty}")

        self.assertEqual(expected, actual, "Product list should match with expected")
        print("4. Test complete")

    def test_8_go_back_continue_shopping(self):
        self.inventory_page.go_to_cart_page()

        print("="*50)
        print("### Go Back Continue Shopping ###")
        print("1. Start test")

        first_url = self.driver.current_url
        print("Current URL: ", first_url )

        self.cart_page.go_to_continue_shopping()

        result = self.login_page.is_logged_in()
        self.assertTrue(result, "User should be in Inventory Page")
        print("2. Successfully go to inventory page")

        second_url = self.driver.current_url
        print("Current URL: ", second_url)
        print("3. Test complete")

    def test_9_go_to_checkout_page(self):
        self.inventory_page.go_to_cart_page()

        print("="*50)
        print("### Go To Checkout Page ###")
        print("1. Start test")

        first_url = self.driver.current_url
        print("Current URL: ", first_url )

        self.cart_page.go_to_checkout_page()

        result = self.checkout_page.is_it_checkout_1_page()
        self.assertTrue(result, "User should be in Checkout Page")
        print("2. Successfully go to checkout page")

        second_url = self.driver.current_url
        print("Current URL: ", second_url)
        print("3. Test complete")

        

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
if __name__ == "__main__":
    unittest.main()

