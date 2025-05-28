import pytest
from playwright.sync_api import Page, expect
import re


def test_edit_device_name(auth_page: Page):
    """Изменение имени устройства и возврат его обратно, с проверкой успешного сохранения."""

    page = auth_page

    # Открытие клиента и переход к устройствам
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Поиск устройства по шаблону
    pattern = re.compile("014 917 927")
    row = page.get_by_role("row", name=pattern)
    row.get_by_role("checkbox").check()

    # Нажатие на кнопку редактирования
    page.get_by_role("button", name="").click()

    # === Шаг 1: изменение имени устройства на c405-Andrey2 ===
    page.locator("#Name").click()
    page.locator("#Name").fill("c405-Andrey2")

    # Эмуляция клика вне поля (по первым вставленным элементам, как в codegen)
    page.get_by_role("insertion").first.click()

    # Сохранение
    page.get_by_role("button", name="Сохранить").click()

    # Проверка успеха
    success_message = page.locator("div").filter(has_text="Устройство успешно сохранено").nth(1)
    expect(success_message).to_be_visible(timeout=5000)

    # === Шаг 2: возврат имени обратно на c405-Andrey ===
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Name").click()
    page.locator("#Name").fill("c405-Andrey")
    page.get_by_role("button", name="Сохранить").click()

    # Повторная проверка
    success_message = page.locator("div").filter(has_text="Устройство успешно сохранено").nth(1)
    expect(success_message).to_be_visible(timeout=5000)
