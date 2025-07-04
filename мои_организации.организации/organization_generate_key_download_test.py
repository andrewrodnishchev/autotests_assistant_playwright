import pytest
from playwright.sync_api import expect

def test_generate_key_download(auth_page):
    page = auth_page

    # Переход в раздел "Устройства"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Открытие контекстного меню устройства
    page.get_by_role("row", name="фильтры тест ").locator("i").click(button="right")

    # Выбор "Сгенерировать ключ"
    page.get_by_role("link", name="Сгенерировать ключ").click()

    # Ожидание и скачивание файла
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Сгенерировать").click()
    download = download_info.value

    # Проверка, что файл был успешно загружен
    assert download.suggested_filename.endswith(".key"), "Ожидался KEY-файл"
