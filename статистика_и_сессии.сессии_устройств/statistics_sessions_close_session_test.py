import pytest
from playwright.sync_api import expect


def test_close_device_session(auth_page):
    page = auth_page

    # Переход в "Сессии устройств"
    page.get_by_role("link", name="Статистика и сессии").click()
    page.get_by_role("link", name="Сессии устройств").click()

    # Поиск устройства
    page.get_by_role("searchbox", name="Поиск:").click()
    page.get_by_role("searchbox", name="Поиск:").fill("014 917 927")
    page.get_by_role("searchbox", name="Поиск:").press("Enter")

    # Закрытие сессии
    page.get_by_role("gridcell", name="014 917 927").click(button="right")
    page.get_by_role("link", name="Закрыть сессию").click()
    page.get_by_role("button", name="Выполнить").click()

    # Проверка уведомления
    success_toast = page.locator("div").filter(has_text="Сессия закрыта").nth(1)
    expect(success_toast).to_be_visible(timeout=5000)
