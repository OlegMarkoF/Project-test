import requests
import os
from .base_page import BasePage
from selenium.webdriver.common.by import By

class DownloadPage(BasePage):
    def download_plugin_link(self):
        download_link = self.find_element(By.XPATH, "//div[contains(@class, 'sbisru-Footer')]//a[contains(text(), 'Скачать локальные версии')]")
        download_link.click()

    def download_sbis_plugin(self):
        plugin_url = "https://update.sbis.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe"
        response = requests.get(plugin_url)
        
        file_path = os.path.join(os.getcwd(), "sbisplugin-setup-web.exe")
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        return file_path

    def verify_plugin_size(self):
        file_path = os.path.join(os.getcwd(), "sbisplugin-setup-web.exe")
        
        assert os.path.exists(file_path), "Плагин не скачался"

        downloaded_file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  
        expected_file_size_mb = 11.48
        
        assert abs(downloaded_file_size_mb - expected_file_size_mb) < 0.01, f"Размер файла {downloaded_file_size_mb:.2f} МБ не совпадает с ожидаемым {expected_file_size_mb} МБ"