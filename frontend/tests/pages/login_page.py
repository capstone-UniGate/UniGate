from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812

from tests.constants import Urls

from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver: webdriver.Chrome) -> None:
        super().__init__(driver)
        # Set the URL after initialization
        self.URL = f"{Urls.BASE_URL}/login"

    # Locators
    LOGIN_FORM = (By.ID, "login-form")

    def is_login_form_visible(self) -> bool:
        """Check if login form is visible on the page"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORM))
        except TimeoutException:
            return False
        return True