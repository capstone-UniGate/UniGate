import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:3000"  # Could be moved to a config file


class CreateGroupPage:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(f"{BASE_URL}/group/create")

    def fill_name(self, name: str):
        name_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "group-name"))
        )
        self.wait.until(EC.element_to_be_clickable((By.ID, "group-name")))
        name_input.clear()
        time.sleep(0.5)
        name_input.send_keys(name)
        time.sleep(0.5)
        return name_input

    def select_course(self, course: str):
        course_select = self.wait.until(
            EC.presence_of_element_located((By.ID, "group-course"))
        )
        course_select.send_keys(course)
        return course_select

    def set_privacy(self, is_public: bool):
        radio_id = "public-radio" if is_public else "private-radio"
        radio = self.wait.until(EC.presence_of_element_located((By.ID, radio_id)))
        radio.click()
        return radio

    def fill_description(self, description: str):
        desc_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "group-description"))
        )
        desc_input.clear()
        desc_input.send_keys(description)
        return desc_input

    def add_tag(self, tag: str):
        try:
            # Try finding the input directly first
            tags_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='tags']"))
            )
        except TimeoutException:
            # If that fails, try finding the container and then the input
            tags_container = self.wait.until(
                EC.presence_of_element_located((By.ID, "group-tags-container"))
            )
            tags_input = tags_container.find_element(By.TAG_NAME, "input")

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='tags']"))
        )
        tags_input.clear()
        tags_input.send_keys(tag)
        tags_input.send_keys(Keys.ENTER)

    def submit_form(self):
        submit_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "create-group-submit"))
        )
        submit_button.click()

    def cancel_form(self):
        cancel_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "create-group-cancel"))
        )
        cancel_button.click()
