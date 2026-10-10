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
from pages.checkout_complete import CheckoutComplete

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
        cls.checkout_complete_page = CheckoutComplete(cls.driver)

    def setUp(self):
        self.base.load()
        self.login_page.login("standard_user", "secret_sauce")

    def test_1_verify_checkout_complete(self):
        self.inventory_page.add_product_to_cart("Sauce Labs Backpack")
        self.inventory_page.add_product_to_cart("Sauce Labs Bike Light")
        self.inventory_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()
        self.checkout_page.input_data_pribadi()
        self.checkout_page.click_continue_checkout()
        self.checkout2_page.click_finish_checkout()

        print("="*50)
        print("### Verify Checkout Complete Page ###")
        print("Precondition : User in Checkout Complete page")
        print("1. Start verifying")
        print("2. Is it checkout complete page?")

        result = self.checkout2_page.is_it_checkout_complete_page()

        self.assertTrue(result, "User should be in checkout complete page")

        print("3. Result: ", result)
        print("4. Test complete")

    def test_2_go_back_home(self):
        self.inventory_page.go_to_cart_page()
        self.cart_page.go_to_checkout_page()
        self.checkout_page.input_data_pribadi()
        self.checkout_page.click_continue_checkout()
        self.checkout2_page.click_finish_checkout()

        print("="*50)
        print("### Go Back Home ###")
        print("Precondition : User in Checkout Complete page")
        print("1. Start verifying")
        print("2. Is it inventory page?")
        self.checkout_complete_page.click_back_home()
        result = self.login_page.is_logged_in()
        self.assertTrue(result, "User should be in checkout complete page")

        print("3. Result: ", result)
        print("4. Complete")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
if __name__ == "__main__":
    unittest.main()

