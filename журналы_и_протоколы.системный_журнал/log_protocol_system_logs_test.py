import os
import pytest
from playwright.sync_api import expect


def test_export_system_log(auth_page, tmp_path):
    page = auth_page

    # Навигация в системный журнал
    page.get_by_role("link", name=" Журналы и протоколы ").click()
    page.get_by_role("link", name=" Системный журнал").click()
    page.get_by_role("link", name="Выгрузить").click()

    # Ожидаем и сохраняем скачанный файл
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Выгрузить").click()
    download = download_info.value
    download_path = os.path.join(tmp_path, download.suggested_filename)
    download.save_as(download_path)

    # Проверка
    assert os.path.exists(download_path), f"Файл не был найден: {download_path}"
    assert os.path.getsize(download_path) > 0, "Скачанный файл пустой"

    print(f"\n✅ Файл системного журнала успешно загружен: {download_path}")
