import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from selenium import webdriver

from pages.base import Base
from pages.login import Login
from pages.inventory import Inventory

class InventoryTest(unittest.TestCase):

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

    def setUp(self):
        self.base.load()
        self.login_page.login("standard_user", "secret_sauce")

    def test_verify_inventory_page(self):
        print("="*50)
        print("### Verify Inventory Page ###")
        print("1. Start verifying")
        result = self.login_page.is_logged_in()

        print("2. Result :", result)

        self.assertTrue(
            result,
            "User should be in Inventory Page"
        )

        print("3. Test completed")


    def test_verify_product_list(self):
        print("="*50)
        print("### Verify Product List ###")
        print("1. Starting verifying")

        products = self.inventory_page.get_product_list()

        self.assertEqual(
            len(products), 
            6,
            "Product list should contain 6 products"
        )

        print("2. Product count: ", len(products))
        print("3. Test complete")

    def test_verify_product_names(self):
        print("="*50)
        print("### Verify Product Names ###")
        print("1. Starting verifying")

        expected = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Fleece Jacket",
            "Sauce Labs Onesie",
            "Test.allTheThings() T-Shirt (Red)"
        ]

        actual = self.inventory_page.get_product_names()

        print("2. Expected product:")
        for product in expected:
            print("-", product)

        print("3. Actual product:")
        for product in actual:
            print("-", product)

        self.assertEqual(
            actual, 
            expected,
            "Product names should match with expected product"
        )
        print("4. Test complete")

    def test_verify_product_prices(self):
        print("="*50)
        print("### Verify Product Prices ###")
        print("1. Starting verifying")

        expected = [
            "$29.99",
            "$9.99",
            "$15.99",
            "$49.99",
            "$7.99",
            "$15.99"
        ]

        actual = self.inventory_page.get_product_prices()

        print("2. Expected product:")
        for price in expected:
            print("-", price)

        print("3. Actual product:")
        for price in actual:
            print("-", price)

        self.assertEqual(
            actual, 
            expected,
            "Product prices should match with expected product price"
        )
        print("4. Test complete")

    def test_verify_product_names_prices(self):
        print("="*50)
        print("### Verify Product Names & Prices ###")
        print("1. Starting verifying")

        expected = [
            ("Sauce Labs Backpack", "$29.99"),
            ("Sauce Labs Bike Light", "$9.99"),
            ("Sauce Labs Bolt T-Shirt", "$15.99"),
            ("Sauce Labs Fleece Jacket", "$49.99"),
            ("Sauce Labs Onesie", "$7.99"),
            ("Test.allTheThings() T-Shirt (Red)", "$15.99")
        ]

        actual = self.inventory_page.get_product_name_price()

        print("2. Expected product:")
        for name, price in expected:
            print(f"- {name} → {price}")

        print("3. Actual product:")
        for name, price in actual:
            print(f"- {name} → {price}")

        self.assertEqual(
            actual, 
            expected,
            "Product name and prices should match with expected"
        )
        print("4. Test complete")

    def test_filter_product(self):
        print("="*50)
        print("### Filter Product ###")
        print("1. Start")
        
        self.inventory_page.filter_product("Name (Z to A)")

        expected = [
            "Test.allTheThings() T-Shirt (Red)",
            "Sauce Labs Onesie",
            "Sauce Labs Fleece Jacket",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Bike Light",
            "Sauce Labs Backpack"
        ]

        actual = self.inventory_page.get_product_names()

        print("2. Expected: ")
        for i in expected:
            print("-", i)

        print("3. Actual: ")
        for i in actual:
            print("-", i)

        self.assertEqual(
            actual,
            expected,
            "Products are not sorted by Name Z to A"
        )

        print("4. Test complete")

    def test_add_product_to_cart(self):
        print("="*50)
        print("### Add Product to Cart ###")
        print("1. Starting test")

        product = "Sauce Labs Backpack"

        self.inventory_page.add_product_to_cart(product)

        print("2. Product added:", product)

        cart_count = self.inventory_page.get_cart_count()

        print("3. Cart count:", cart_count)

        self.assertEqual(
            cart_count,
            1,
            "Cart should contain 1 product"
        )

        print("4. Product successfully added to cart")
        print("5. Test complete")

    def test_remove_product(self):
        print("="*50)
        print("### Remove Product ###")
        print("1. Starting test")

        product = "Sauce Labs Bike Light"

        self.inventory_page.add_product_to_cart(product)

        print("2. Product added:", product)

        cart_count_before = self.inventory_page.get_cart_count()

        print("3. Cart count:", cart_count_before)

        print("4. Product removed:", product)

        self.inventory_page.remove_product(product)

        cart_count_after = self.inventory_page.get_cart_count()

        print("5. Cart count:", cart_count_after)

        self.assertEqual(cart_count_after, cart_count_before - 1, "Failed remove product")

        print("6. Product successfully removed")
        print("7. Test complete")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
if __name__ == "__main__":
    unittest.main()

