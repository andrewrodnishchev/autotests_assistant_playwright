import pytest
from playwright.sync_api import Page, expect

def test_bulk_group_change(auth_page: Page):
    page = auth_page

    # Переход в раздел "Устройства"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Отмечаем 2 устройства
    page.get_by_role("row", name="076 897 034").get_by_role("checkbox").check()
    page.get_by_role("row", name="135 026 892").get_by_role("checkbox").check()

    # Нажимаем кнопку редактирования
    page.get_by_role("button", name="").click()

    # Выбор "Не изменять" → "группа"
    page.get_by_title("Не изменять", exact=True).click()
    page.get_by_role("treeitem", name="группа 1").click()

    # Выполняем действие
    page.get_by_role("button", name="Выполнить").click()

    # Проверяем всплывающее сообщение об успехе
    expect(page.locator("div").filter(has_text="Успешно изменено устройств:").nth(1)).to_be_visible()
