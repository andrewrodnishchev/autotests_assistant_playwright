import pytest
from playwright.sync_api import Page, expect


def test_edit_device_department_access(auth_page: Page):
    page = auth_page

    # Переход в "Устройства"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Правый клик по ячейке "917 927" и переход к просмотру
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Просмотр").click()

    # Открытие доступа для сотрудников
    page.get_by_role("link", name="Доступ для своих сотрудников").click()

    # Включение доступа (Yes → Да)
    page.get_by_role("row", name="Новый отдел Нет ").get_by_role("checkbox").check()
    page.get_by_role("row", name="Изолированный отдел Нет ").get_by_role("checkbox").check()
    page.get_by_role("row", name="отдел2 Нет ").get_by_role("checkbox").check()
    page.get_by_role("button", name="Изменить доступ").click()
    page.get_by_role("button", name="Сохранить").click()

    # Проверка уведомления об успешном изменении
    expect(page.locator("div").filter(has_text="Настройки доступа успешно изменены (3 шт.)").nth(1)).to_be_visible()

    # Отключение доступа (Yes → No)
    page.get_by_role("row", name="Новый отдел Да 111 ").get_by_role("checkbox").check()
    page.get_by_role("row", name="Изолированный отдел Да 111 ").get_by_role("checkbox").check()
    page.get_by_role("row", name="отдел2 Да 111 ").get_by_role("checkbox").check()
    page.get_by_role("button", name="Изменить доступ").click()
    page.locator("#AccessType").select_option("No")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка второго уведомления
    expect(page.locator("div").filter(has_text="Настройки доступа успешно изменены (3 шт.)").nth(1)).to_be_visible()
