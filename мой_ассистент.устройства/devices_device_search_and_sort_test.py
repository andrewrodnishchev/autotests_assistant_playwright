from playwright.sync_api import expect
import pytest

def test_device_search_and_sort(auth_page):
    page = auth_page

    # Переход в раздел "Мой ассистент" → "Устройства"
    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Устройства").click()

    # Поиск по идентификатору
    searchbox = page.get_by_role("searchbox", name="Поиск:")
    searchbox.click()
    searchbox.fill("014")
    searchbox.press("Enter")

    # Проверка, что отображается нужный результат
    expect(page.get_by_role("gridcell", name=" 014 917")).to_be_visible(timeout=5000)

    # Очистка поиска
    searchbox.click()
    searchbox.fill("")

    # Сортировка по заголовкам таблицы
    columns_to_sort = [
        "Идентификатор ", "Идентификатор ",
        "Наименование ", "Наименование ",
        "Лицензия ", "Лицензия ",
        "Комментарий ", "Комментарий "
    ]

    for column_name in columns_to_sort:
        page.get_by_role("gridcell", name=column_name).click()
        # можно вставить проверку на изменение порядка, если нужно
