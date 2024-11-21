from .base_page import BasePage


class GroupsPage(BasePage):
    URL = "http://localhost:3000/group"

    def load(self) -> None:
        # Load the My Groups page.
        self.driver.get(self.URL)
