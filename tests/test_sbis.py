# tests/test_sbis.py

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.contacts_page import ContactsPage
from pages.download_page import DownloadPage

@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def test_sbis_website_navigation(browser):
    main_page = MainPage(browser)
    
    # Переходим на главную страницу и кликаем "Контакты"
    main_page.go_to_site("https://sbis.ru/")
    main_page.click_contacts()

    # Ожидаем появления модального окна с контактами
    contact_menu_items = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sbisru-Header-ContactsMenu__items-visible"))
    )

    # Кликаем по ссылке контактов с использованием JavaScript для избежания ошибок
    contact_link = browser.find_element(By.CSS_SELECTOR, ".sbisru-link.sbis_ru-link")
    browser.execute_script("arguments[0].click();", contact_link)

    # Ожидаем появления баннера Тензор и кликаем по нему
    tensor_banner = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "sbisru-Contacts__logo-tensor"))
    )
    tensor_banner.click()

    # Переключаемся на новую вкладку (после клика на баннер)
    browser.switch_to.window(browser.window_handles[1])

    # Проверяем текущий URL
    assert browser.current_url == "https://tensor.ru/", "URL не совпадает!"

    # Ожидаем появления блока с классом 'tensor_ru-Index__block4-bg'
    block = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tensor_ru-Index__block4-bg"))
    )

    # Находим ссылку "Подробнее"
    more_link = block.find_element(By.XPATH, ".//a[contains(@class, 'tensor_ru-link') and text()='Подробнее']")

    # Кликаем по ссылке
    browser.execute_script("arguments[0].click();", more_link)

    # Ожидаем загрузки страницы "О компании"
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tensor_ru-About__block3"))
    )

    # Проверяем текущий URL
    assert browser.current_url == "https://tensor.ru/about", "URL не совпадает!"

    # Ожидаем появления блока с классом "tensor_ru-About__block3"
    block = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tensor_ru-About__block3"))
    )
    
    # Находим все изображения в этом блоке
    images = block.find_elements(By.TAG_NAME, "img")
    
    # Получаем размеры первого изображения для сравнения
    first_image_size = None
    
    for image in images:
        # Получаем размеры изображения
        width = image.size['width']
        height = image.size['height']
        
        print(f"Image: {image.get_attribute('src')} - Width: {width}, Height: {height}")
        
        if first_image_size is None:
            first_image_size = (width, height)
        else:
            # Проверяем, совпадают ли размеры с первым изображением
            assert (width, height) == first_image_size, "Изображения имеют разные размеры!"
    
    print("Все изображения имеют одинаковый размер.")

def test_check_region_and_partners(browser):
    contacts_page = ContactsPage(browser)
    
    # Переходим на главную страницу и кликаем "Контакты"
    contacts_page.go_to_site("https://sbis.ru/")
    
    contacts_page.click_contacts()

    # Проверка региона и списка партнеров
    contacts_page.check_region_and_partners()
    
    # Выбор региона Камчатский край и проверка изменений
    contacts_page.select_region()
    contacts_page.choose_kamchatka()

def test_download_plugin(browser):
    download_page = DownloadPage(browser)
    
    # Переходим на главную страницу и скачиваем плагин
    download_page.go_to_site("https://sbis.ru/")
    
    download_page.download_plugin_link()
    
    file_path = download_page.download_sbis_plugin()
    
    # Проверяем размер скачанного плагина
    download_page.verify_plugin_size()