from .base_page import BasePage
from selenium.webdriver.common.by import By

class MainPage(BasePage):
    
    def click_contacts(self):
        contacts_menu = self.find_element(By.CLASS_NAME, "sbisru-Header-ContactsMenu")
        contacts_menu.click()