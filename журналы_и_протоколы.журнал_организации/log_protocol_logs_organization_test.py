import os
import pytest
from playwright.sync_api import expect


def test_export_org_log(auth_page, tmp_path):
    page = auth_page

    # Навигация в журнал
    page.get_by_role("link", name=" Журналы и протоколы ").click()
    page.get_by_role("link", name=" Журнал организации").click()
    page.get_by_role("link", name="Выгрузить").click()

    # Ожидаем загрузку
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Выгрузить").click()
    download = download_info.value

    # Сохраняем файл в tmp_path
    download_path = os.path.join(tmp_path, download.suggested_filename)
    download.save_as(download_path)

    # Проверки
    assert os.path.exists(download_path), f"Файл не найден: {download_path}"
    assert os.path.getsize(download_path) > 0, "Файл пустой"

    print(f"\n✅ Файл загружен: {download_path}")
