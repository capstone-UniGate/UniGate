from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from tests.constants import Urls


class SeeMyGroupsPage:
    URL = Urls.SEE_MY_GROUP
    # Locators
    HEADING = (By.CSS_SELECTOR, "h1")
    LOADING_INDICATOR = (By.CSS_SELECTOR, "[data-testid='loading-indicator']")
    GROUP_CARDS = (By.CSS_SELECTOR, "[data-testid='group-card']")
    CREATE_GROUP_BUTTON = (By.CSS_SELECTOR, "[data-testid='create-group-button']")

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self) -> None:
        self.driver.get(self.URL)

    def is_heading_visible(self) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.HEADING)
            ).is_displayed()
        except Exception:  # noqa: BLE001
            return False

    def is_loading(self) -> bool | WebElement:
        try:
            return self.driver.find_element(*self.LOADING_INDICATOR).is_displayed()
        except Exception:  # noqa: BLE001
            return False

    # def has_error(self) -> bool | WebElement:
    #     """Check if error message is visible"""
    #     try:
    #         return self.driver.find_element(*self.ERROR_MESSAGE).is_displayed()
    #     except Exception:
    #         return False

    def get_group_cards(self) -> list[WebElement]:
        """Get all group cards on the page"""
        self.wait.until(EC.presence_of_element_located(self.GROUP_CARDS))
        return self.driver.find_elements(*self.GROUP_CARDS)

    def click_create_group(self) -> None:
        """Click the Create Group button"""
        button = self.wait.until(EC.element_to_be_clickable(self.CREATE_GROUP_BUTTON))
        button.click()
