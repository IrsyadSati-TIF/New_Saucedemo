import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from selenium import webdriver

from pages.base import Base
from pages.login import Login
from pages.inventory import Inventory

class LoginTest(unittest.TestCase):

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

    def setUp(self):
        self.base.load()

    def test_successful_login(self):
        print("="*50)
        print("### Successful Login ###")
        print("1. Starting login test")

        self.login_page.login("standard_user", "secret_sauce")

        print("2. Login completed")
        print("3. Current URL:", self.driver.current_url)

        result = self.login_page.is_logged_in()

        print("4. Is logged in:", result)

        self.assertTrue(
            result,
            "User should be logged in successfully"
        )

        print("5. Test completed")


    def test_failed_login(self):
        print("="*50)
        print("### Failed Login ###")
        print("1. Starting login test")

        self.login_page.login(
            "wrong_username",
            "wrong_password"
        )

        print("2. Login failed")
        print("3. Current URL:", self.driver.current_url)

        result = self.login_page.is_logged_in()
        error = self.login_page.get_error_message()

        print("4. Is logged in:", result)

        self.assertFalse(
            result,
            "User should not be logged in with invalid credentials"
        )

        self.assertEqual(
            error,
            "Epic sadface: Username and password do not match any user in this service"
        )

        print("5.", error)
        print("6. Test completed")

    def test_empty_username(self):
        print("="*50)
        print("### Failed Login - Empty Username ###")
        print("1. Starting login test")

        self.login_page.login(
            "",
            "secret_sauce"
        )

        print("2. Login failed")
        print("3. Current URL:", self.driver.current_url)

        result = self.login_page.is_logged_in()
        error = self.login_page.get_error_message()

        print("4. Is logged in:", result)

        self.assertFalse(
            result,
            "User should not be logged in with empty username"
        )

        self.assertEqual(
            error,
            "Epic sadface: Username is required"
        )
        
        print("5.", error)
        print("6. Test completed")

    def test_empty_password(self):
        print("="*50)
        print("### Failed Login - Empty Password ###")
        print("1. Starting login test")

        self.login_page.login(
            "standard_user",
            ""
        )

        print("2. Login failed")
        print("3. Current URL:", self.driver.current_url)

        result = self.login_page.is_logged_in()
        error = self.login_page.get_error_message()

        print("4. Is logged in:", result)

        self.assertFalse(
            result,
            "User should not be logged in with empty password"
        )
        self.assertEqual(
            error,
            "Epic sadface: Password is required"
        )
        
        print("5.", error)
        print("6. Test completed")

    def test_locked_user(self):
        print("="*50)
        print("### Failed Login - Locked User ###")
        print("1. Starting login test")

        self.login_page.login(
            "locked_out_user",
            "secret_sauce"
        )

        print("2. Login failed")
        print("3. Current URL:", self.driver.current_url)

        result = self.login_page.is_logged_in()
        error = self.login_page.get_error_message()

        print("4. Is logged in:", result)

        self.assertFalse(
            result,
            "User should not be logged in with locked user"
        )

        self.assertEqual(
            error,
            "Epic sadface: Sorry, this user has been locked out."
        )
        
        print("5.", error)
        print("6. Test completed")

    def test_successful_logout(self):
        print("="*50)
        print("### Successful Logout ###")
        print("1. Starting login")

        self.login_page.login("standard_user", "secret_sauce")

        print("2. Login complete")
        print("3. Starting logout test")

        self.inventory_page.logout()

        print("4. Logout complete")
        print("5. Current URL:", self.driver.current_url)

        result = self.login_page.is_logged_out()

        print("6. Is logged out:", result)

        self.assertTrue(
            result,
            "User should be logged out"
        )

        print("7. Test completed")


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
if __name__ == "__main__":
    unittest.main()

