import pytest
from playwright.sync_api import expect
import time

def test_export_statistics(auth_page):
    page = auth_page

    # Переход в "Статистика"
    page.get_by_role("link", name=" Статистика и сессии ").click()
    page.get_by_role("link", name=" Статистика").click()

    time.sleep(2)

    # Выгрузка статистики
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Экспорт статистики в файл").click()
    download = download_info.value

    # Проверка: файл действительно начал скачиваться
    assert download.suggested_filename, "Скачивание не началось — отсутствует имя файла"
