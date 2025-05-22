import pytest
from playwright.sync_api import Page, expect


def test_remove_and_add_employee_to_department(auth_page: Page):
    """Удаление сотрудника из отдела и повторное добавление."""

    page = auth_page

    email = "testast@mailforspam.com"

    # Переход в отдел
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Сотрудники").click()
    page.get_by_text("Новый отдел").click()

    # Удаление сотрудника из отдела
    page.get_by_role("gridcell", name=email).click(button="right")
    page.get_by_role("link", name="Удалить из отдела").click()
    page.get_by_role("button", name="Удалить").click()
    expect(page.get_by_text("Удалено 1 сотрудников")).to_be_visible()

    # Переход в отдел для повторного добавления
    page.get_by_role("gridcell", name="Новый отдел").click(button="right")
    page.get_by_role("link", name="Просмотр").click()
    page.get_by_role("link", name="Сотрудники").nth(1).click()
    page.get_by_role("link", name="Добавить сотрудника").click()

    # Добавление нужного сотрудника обратно
    row = page.get_by_role("row", name="test_fn test_ln testast@")
    row.get_by_role("checkbox").check()
    page.get_by_role("link", name="Добавить").click()
    expect(page.get_by_text("Сотрудники успешно добавлены (1 шт.)", exact=True)).to_be_visible(timeout=5000)
