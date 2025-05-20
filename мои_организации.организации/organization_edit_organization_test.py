import pytest
from playwright.sync_api import Page, expect


def test_edit_organization_phone(auth_page: Page):
    """Изменение телефона организации и проверка успешного сохранения."""
    page = auth_page

    # Переход в настройки организации
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Изменить").click()

    # Изменение
    page.locator("#Phone").click()
    page.locator("#Phone").fill("777")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка сообщения об успехе
    success_message = page.locator("div").filter(has_text="Организация успешно сохранена").nth(1)
    expect(success_message).to_be_visible(timeout=5000)
