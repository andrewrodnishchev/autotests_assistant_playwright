import pytest
from playwright.sync_api import Page, expect
import re


def test_edit_device_name(auth_page: Page):
    """Изменение имени устройства и проверка успешного сохранения."""
    page = auth_page

    # Открытие клиента
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Редактирование первого устройства
    pattern = re.compile(r".*014 917 927 c405-Andrey2.*")
    row = page.get_by_role("row", name=pattern)
    row.get_by_role("checkbox").check()
    page.get_by_role("button", name="").click()

    # Изменение имени
    page.locator("#Name").fill("c405-Andrey2")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка успеха
    success_message = page.locator("div").filter(has_text="Устройство успешно сохранено").nth(1)
    expect(success_message).to_be_visible(timeout=5000)
