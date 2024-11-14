from .base_page import BasePage
from selenium.webdriver.common.by import By

class ContactsPage(BasePage):
    def select_region(self):
        region_element = self.find_element(By.CSS_SELECTOR, "span.sbis_ru-Region-Chooser__text.sbis_ru-link")
        region_element.click()

    def choose_kamchatka(self):
        kamchatka_element = self.find_element(By.XPATH, "//span[contains(@class, 'sbis_ru-link') and contains(text(), 'Камчатский край')]")
        kamchatka_element.click()

    def check_region_and_partners(self):
        region_element = self.find_element(By.CSS_SELECTOR, "span.sbis_ru-Region-Chooser__text.sbis_ru-link")
        
        assert region_element.text.strip(), "Регион не определился"

        partners_list = self.find_element(By.ID, "contacts_list")
        assert partners_list.is_displayed(), "Список партнеров не отображается"