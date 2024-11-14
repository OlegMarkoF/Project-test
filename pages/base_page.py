from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((by, value)))

    def find_elements(self, by, value):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((by, value)))

    def go_to_site(self, url):
        self.driver.get(url)