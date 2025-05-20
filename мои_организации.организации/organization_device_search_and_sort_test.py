import pytest
from playwright.sync_api import expect

def test_device_search_and_sort(auth_page):
    page = auth_page

    # Переход к организации
    page.get_by_role("link", name="тест андрей").click()

    # Переход в раздел "Устройства"
    page.get_by_role("link", name="Устройства").click()

    # Поиск устройства
    search_input = page.get_by_placeholder("Найти устройство").first
    search_input.click()
    search_input.fill("014 917 927")
    search_input.press("Enter")

    # Убедимся, что нужное устройство появилось
    expect(page.get_by_role("gridcell", name="917 927")).to_be_visible()

    # Очистить поиск
    search_input.click()
    search_input.fill("")
    search_input.press("Enter")

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
        page.get_by_role("gridcell", name=f"{col}: активировать для сортировки столбца по возрастанию").click()
        page.get_by_role("gridcell", name=f"{col}: активировать для сортировки столбца по убыванию").click()
