from selenium.webdriver.common.by import By  # Add this import

from .base_page import BasePage


class MyGroupsPage(BasePage):
    URL = "http://localhost:3000/group/see-my-group"
    CREATE_NEW_GROUP_BUTTON = (By.CSS_SELECTOR, "[data-testid='create-group-btn']")

    def load(self) -> None:
        # Load the My Groups page.
        self.driver.get(self.URL)

    def click_create_new_group(self) -> None:
        # Click the 'Create New Group' button.
        self.driver.find_element(*self.CREATE_NEW_GROUP_BUTTON).click()
