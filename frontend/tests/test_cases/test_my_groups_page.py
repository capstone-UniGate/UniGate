from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from tests.pages.create_group_page import CreateGroupPage
from tests.pages.my_groups_page import MyGroupsPage
from tests.utils import wait_until_ec


def test_see_my_groups(driver: webdriver.Chrome) -> None:
    my_groups_page = MyGroupsPage(driver)
    my_groups_page.load()

    # wait for groups cars
    wait_until_ec(driver, presence_of_element_located, (By.CLASS_NAME, "bg-card"))
    groups = driver.find_elements(By.CLASS_NAME, "bg-card")
    assert len(groups) == 10


def test_create_group_form(driver: webdriver.Chrome) -> None:
    create_group_page = CreateGroupPage(driver)
    create_group_page.load()

    # Wait for form element with correct ID
    wait_until_ec(driver, presence_of_element_located, (By.ID, "group-name"))

    name_input = create_group_page.fill_name("Test Group")
    desc_input = create_group_page.fill_description("This is a test group description")

    assert name_input.get_property("value") == "Test Group"
    assert desc_input.get_property("value") == "This is a test group description"


def test_create_group_form_submission(driver: webdriver.Chrome):
    page = CreateGroupPage(driver)
    page.load()

    # Wait for the first form element to be present
    wait_until_ec(driver, presence_of_element_located, (By.ID, "group-name"))

    # Fill form using page object methods
    name_input = page.fill_name("Test Study Group")
    course_select = page.select_course("course1")
    privacy_radio = page.set_privacy(True)  # public
    desc_input = page.fill_description("This is a test study group")
    page.add_tag("python")

    # Verify inputs
    assert name_input.get_property("value") == "Test Study Group"
    assert course_select.get_property("value") == "course1"
    assert privacy_radio.is_selected()
    assert desc_input.get_property("value") == "This is a test study group"

    # Submit form
    page.submit_form()

    # Add assertions for successful submission
    assert "/group" in driver.current_url


def test_create_group_validation(driver: webdriver.Chrome):
    page = CreateGroupPage(driver)
    page.load()

    # Try to submit empty form
    page.submit_form()

    # Verify validation messages
    # Add assertions based on your validation message elements
