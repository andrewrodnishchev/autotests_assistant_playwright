import pytest
from playwright.sync_api import Page, expect


def test_toggle_support_notifications(auth_page: Page):
    page = auth_page

    # Переход в профиль
    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Профиль").click()

    # Переключаем настройку получения уведомлений
    page.get_by_role("insertion").click()
    expect(page.locator("div.toast-message", has_text="Настройка Получать уведомления на email о заявках в поддержку успешно изменена")).to_be_visible(timeout=5000)

    # Переключаем обратно
    page.get_by_role("insertion").click()
    expect(page.locator("div.toast-message", has_text="Настройка Получать уведомления на email о заявках в поддержку успешно изменена")).to_be_visible(timeout=5000)
