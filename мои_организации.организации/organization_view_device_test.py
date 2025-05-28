import pytest
from playwright.sync_api import expect


def test_device_details_check(auth_page):
    page = auth_page

    # Переход к нужному устройству
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Просмотр").click()

    # Проверка значений в input-элементах
    expect(page.locator("#HID")).to_have_value("014 917 927")
    expect(page.locator("#Name")).to_have_value("c405-Andrey")
    expect(page.locator("#DomainName")).to_have_value("c405-Andrey")

