import pytest
from playwright.sync_api import expect

def test_send_message_to_device(auth_page):
    page = auth_page

    # Навигация в раздел устройств
    page.get_by_role("link", name=" Администрирование ").click()
    page.get_by_role("link", name=" Устройства").click()

    # Поиск устройства по номеру
    searchbox = page.get_by_role("searchbox", name="Поиск:")
    searchbox.click()
    searchbox.fill("014 917 927")
    searchbox.press("Enter")

    # Отметить чекбокс нужной строки
    row = page.get_by_role("row", name=" 014 917 927")
    row.get_by_role("checkbox").check()

    # Отправить сообщение
    page.get_by_role("button", name="Отправить сообщение").click()
    page.locator("#Text").fill("тест")
    page.get_by_role("button", name="Отправить", exact=True).click()

    # Проверка успешного сообщения
    success_msg = page.locator("div.toast-message", has_text="Успешно отправлено сообщение для нескольких устройств (1 шт.)")
    expect(success_msg).to_be_visible(timeout=5000)
