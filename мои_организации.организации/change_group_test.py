import pytest
from playwright.sync_api import expect


def test_edit_and_revert_device_group_name(auth_page):
    page = auth_page

    # Переход в организацию "тест андрей"
    page.get_by_role("link", name="тест андрей").click()

    # Переход в раздел "Устройства"
    page.get_by_role("link", name="Устройства").click()

    # Просмотр и редактирование группы "тест 1"
    page.get_by_role("row", name="тест 1 ").locator("i").click()
    page.get_by_role("link", name="Просмотр").click()
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Name").click()
    page.locator("#Name").fill("тест 1.1")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка уведомления об успешном сохранении
    success_alert = page.locator("div").filter(has_text="Группа устройств успешно изменена").nth(1)
    expect(success_alert).to_be_visible()

    # Возврат назад
    page.get_by_role("link", name="Назад").click()

    # Проверка переименованной строки "тест 1.1"
    page.get_by_role("row", name="тест 1.1 ").locator("i").click()
    page.get_by_role("link", name="Просмотр").click()
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Name").click()
    page.locator("#Name").fill("тест 1")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка повторного успешного сохранения
    success_alert = page.locator("div").filter(has_text="Группа устройств успешно изменена").nth(1)
    expect(success_alert).to_be_visible()
