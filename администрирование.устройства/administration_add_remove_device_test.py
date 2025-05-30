import pytest
from playwright.sync_api import expect
import time

def test_add_device_to_org(auth_page):
    page = auth_page

    # Переход в "Устройства"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Удаление устройства
    page.get_by_role("gridcell", name="135 026 892").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_role("button", name="Удалить").click()

    # Переход в администрирование
    page.get_by_role("link", name="Администрирование").click()
    page.get_by_role("link", name="Устройства").nth(0).click()

    # Поиск устройства
    searchbox = page.get_by_role("searchbox", name="Поиск:")
    searchbox.fill("135 026 892")
    searchbox.press("Enter")

    # Отметить чекбокс
    row = page.get_by_role("row", name="135 026 892")
    row.get_by_role("checkbox").check()

    # Добавить в организацию
    page.get_by_role("button", name="Добавить в организацию").click()

    # Выбор из выпадающего списка
    page.get_by_role("button", name="Сервисная").click()

    time.sleep(2)
    page.locator("li.opt label", has_text="тест андрей").nth(1).click()

    # Снять защиту
    page.locator("#PreventChangingSecuritySettings").get_by_role("insertion").click()

    # Выполнить действие
    page.get_by_role("button", name="Выполнить").click()

    # Проверка сообщения об успехе
    success_msg = page.locator("div.toast-message", has_text="Успешно добавлено/обновлено 1 устройство.")
    expect(success_msg).to_be_visible(timeout=7000)
