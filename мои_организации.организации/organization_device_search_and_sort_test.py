import time
import pytest
from playwright.sync_api import expect

def test_device_search_and_sort(auth_page):
    page = auth_page

    # Переход к организации
    page.get_by_role("link", name="тест андрей").click()
    time.sleep(0.5)

    # Переход в раздел "Устройства"
    page.get_by_role("link", name="Устройства").click()
    time.sleep(1)

    # Поиск устройства
    search_input = page.get_by_placeholder("Найти устройство").first
    search_input.click()
    time.sleep(0.3)
    search_input.fill("014 917 927")
    time.sleep(0.3)
    search_input.press("Enter")
    time.sleep(1)

    # Убедимся, что нужное устройство появилось
    expect(page.get_by_role("gridcell", name="917 927")).to_be_visible(timeout=5000)
    time.sleep(0.5)

    # Очистить поиск
    search_input.click()
    time.sleep(0.3)
    search_input.fill("")
    time.sleep(0.3)
    search_input.press("Enter")
    time.sleep(1)

    # Проверка сортировок
    sort_columns = [
        "Идентификатор",
        "Наименование",
        "Политика доступа",
        "Политика инвентаризации",
        "Сетевое имя",
        "Домен",
        "Лицензия",
    ]

    for col in sort_columns:
        asc_sort = page.get_by_role("gridcell", name=f"{col}: активировать для сортировки столбца по возрастанию")
        desc_sort = page.get_by_role("gridcell", name=f"{col}: активировать для сортировки столбца по убыванию")

        expect(asc_sort).to_be_visible(timeout=5000)
        asc_sort.click()
        time.sleep(0.3)

        expect(desc_sort).to_be_visible(timeout=5000)
        desc_sort.click()
        time.sleep(0.3)
