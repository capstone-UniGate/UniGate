from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from tests.pages.groups_page import GroupsPage
from tests.utils import wait_until_ec


def test_groups_page(driver: webdriver.Chrome) -> None:
    groups_page = GroupsPage(driver)
    groups_page.load()

    # wait for groups cars
    wait_until_ec(driver, presence_of_element_located, (By.CLASS_NAME, "bg-card"))
    groups = driver.find_elements(By.CLASS_NAME, "bg-card")
    assert len(groups) == 10
