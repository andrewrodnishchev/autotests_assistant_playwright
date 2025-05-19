import pytest
from playwright.sync_api import Page, expect


def test_send_message_to_devices(auth_page: Page):
    """Отправка сообщений нескольким устройствам и одному устройству."""
    page = auth_page

    # Переход к разделу "Устройства"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Выбор двух устройств и отправка общего сообщения
    page.get_by_role("row", name="076 897 034 Samsung SM-").get_by_role("checkbox").check()
    page.get_by_role("row", name="014 917 927 c405-Andrey2").get_by_role("checkbox").check()
    page.get_by_role("button", name="").click()  # Кнопка "Отправить сообщение"
    page.locator("#Text").click()
    page.locator("#Text").fill("тест1")
    page.get_by_role("button", name="Отправить").click()

    expect(
        page.locator("div").filter(
            has_text="Успешно отправлено сообщение для нескольких устройств (2 шт.)"
        ).nth(1)
    ).to_be_visible(timeout=5000)

    # Отправка сообщения через контекстное меню одному устройству
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Отправить сообщение").click()
    page.locator("#Text").click()
    page.locator("#Text").fill("тест2")
    page.get_by_role("button", name="Отправить").click()

    expect(
        page.locator("div").filter(
            has_text="Сообщение успешно отправлено"
        ).nth(1)
    ).to_be_visible(timeout=5000)
