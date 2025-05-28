import pytest
import time
from playwright.sync_api import Page, expect


def test_remove_and_add_employee_to_department(auth_page: Page):
    """Удаление сотрудника из отдела и повторное добавление."""

    page = auth_page
    email = "testast@mailforspam.com"

    # Переход в отдел
    page.get_by_role("link", name="тест андрей").click()
    time.sleep(0.5)

    page.get_by_role("link", name="Сотрудники").click()
    time.sleep(1)

    page.get_by_text("Новый отдел").click()
    time.sleep(1)

    # Удаление сотрудника из отдела
    page.get_by_role("gridcell", name=email).click(button="right")
    time.sleep(0.3)

    page.get_by_role("link", name="Удалить из отдела").click()
    time.sleep(0.3)

    page.get_by_role("button", name="Удалить").click()
    time.sleep(0.5)

    expect(page.get_by_text("Удалено 1 сотрудников")).to_be_visible(timeout=5000)
    time.sleep(0.5)

    # Переход в отдел для повторного добавления
    page.get_by_role("gridcell", name="Новый отдел").click(button="right")
    time.sleep(0.3)

    page.get_by_role("link", name="Просмотр").click()
    time.sleep(0.5)

    page.get_by_role("link", name="Сотрудники").nth(1).click()
    time.sleep(0.5)

    page.get_by_role("link", name="Добавить сотрудника").click()
    time.sleep(1)

    # Добавление нужного сотрудника обратно
    row = page.get_by_role("row", name="test_fn test_ln testast@")
    row.get_by_role("checkbox").check()
    time.sleep(0.3)

    page.get_by_role("link", name="Добавить").click()
    time.sleep(0.5)

    expect(page.get_by_text("Сотрудники успешно добавлены (1 шт.)", exact=True)).to_be_visible(timeout=5000)
