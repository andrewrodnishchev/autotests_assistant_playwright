import pytest
from playwright.sync_api import expect

def test_send_sms_to_device(auth_page):
    page = auth_page

    # Навигация по интерфейсу
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Коллекции").click()
    page.get_by_text("информация об устройстве").click()

    # Правая кнопка по устройству и отправка первого сообщения
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Отправить сообщение").click()
    page.locator("#Text").fill("тест смс")
    page.get_by_role("button", name="Отправить").click()

    # Проверка появления уведомления
    expect(page.locator("div.toast-message", has_text="Сообщение успешно отправлено")).to_be_visible()

    # Отметка чекбокса и повторная отправка
    page.get_by_role("checkbox").check()
    page.get_by_role("button", name="").click()
    page.locator("#Text").fill("тест смс 2")
    page.get_by_role("button", name="Отправить").click()

    # Проверка второго уведомления
    expect(page.locator("div.toast-message", has_text="Сообщение успешно отправлено на 1 устройств")).to_be_visible()
