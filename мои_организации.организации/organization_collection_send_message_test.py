import pytest
from playwright.sync_api import Page, expect


def test_send_sms_to_device(auth_page: Page):
    page = auth_page

    # Навигация по интерфейсу
    page.get_by_role("link", name="тест андрей").click()
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Коллекции").click()
    page.wait_for_timeout(500)
    page.get_by_text("информация об устройстве").click()
    page.wait_for_timeout(500)

    # Правая кнопка по нужному устройству и отправка первого сообщения
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Отправить сообщение").click()
    page.wait_for_timeout(300)
    page.locator("#Text").fill("тест смс")
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Отправить").click()
    page.wait_for_timeout(500)

    # Проверка появления уведомления
    expect(page.locator("div.toast-message", has_text="Сообщение успешно отправлено")).to_be_visible(timeout=5000)
    page.wait_for_timeout(1000)

    # Чекбокс нужного устройства (точно у строки с нужным HID)
    row = page.locator("tr", has_text="014 917 927")
    row.locator("input.js-chk[type='checkbox']").check()
    page.wait_for_timeout(500)

    # Отправка второго сообщения через кнопку
    page.get_by_role("button", name="").click()
    page.wait_for_timeout(300)
    page.locator("#Text").fill("тест смс 2")
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Отправить").click()
    page.wait_for_timeout(500)

    # Проверка второго уведомления
    expect(page.locator("div.toast-message", has_text="Сообщение успешно отправлено на 1 устройств")).to_be_visible(timeout=5000)
    page.wait_for_timeout(1000)
