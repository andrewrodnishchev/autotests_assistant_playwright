import pytest
from playwright.sync_api import Page, expect


def test_change_password(auth_page: Page):
    page = auth_page

    # Переход: Мой ассистент → Профиль → Безопасность
    page.get_by_role("link", name="Мой ассистент").click()
    page.get_by_role("link", name="Профиль").click()
    page.get_by_role("link", name="Безопасность").click()
    page.get_by_role("link", name="Изменить пароль").click()

    # Ввод пароля (старого и нового)
    old_password = "1"
    new_password = "1"

    page.locator("#OldPassword").fill(old_password)
    page.locator("#NewPassword").fill(new_password)
    page.locator("#ConfirmPassword").fill(new_password)

    page.get_by_role("button", name="Сохранить").click()

    # Проверка всплывающего сообщения
    expect(
        page.locator("div.toast-message", has_text="Пароль успешно изменен")
    ).to_be_visible(timeout=5000)
