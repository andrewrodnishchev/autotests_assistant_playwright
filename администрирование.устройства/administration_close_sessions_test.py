import pytest
from playwright.sync_api import expect
import time

def test_close_all_sessions(auth_page):
    page = auth_page

    # Переход в Администрирование > Устройства
    page.get_by_role("link", name=" Администрирование ").click()
    page.get_by_role("link", name=" Устройства").click()

    # Поиск устройства по номеру
    searchbox = page.get_by_role("searchbox", name="Поиск:")
    searchbox.click()
    searchbox.fill("014 917 927")
    searchbox.press("Enter")

    time.sleep(3)
    # Правый клик по устройству
    page.get_by_role("gridcell", name="014 917 927").click(button="right")

    # Клик "Закрыть все сессии"
    page.get_by_role("link", name="Закрыть все сессии").click()

    # Подтверждение действия
    page.get_by_role("button", name="Выполнить").click()

    # Проверка появления уведомления об успешном закрытии сессий
    expect(page.locator("div", has_text="Сессии закрыты").nth(1)).to_be_visible(timeout=5000)
