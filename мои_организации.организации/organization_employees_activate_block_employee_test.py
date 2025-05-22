import pytest
from playwright.sync_api import Page, expect

def test_block_and_activate_employee(auth_page: Page):
    """Блокировка и активация сотрудника."""
    page = auth_page

    # Переход в нужную организацию
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Сотрудники").click()

    # Блокировка сотрудника
    email = "ast30@mailforspam.com"
    page.get_by_role("gridcell", name=email).nth(1).click(button="right")
    page.get_by_role("link", name="Заблокировать").click()
    page.get_by_role("button", name="Заблокировать").click()

    toast_block = page.get_by_text("Сотрудник успешно заблокирован", exact=True)
    expect(toast_block).to_be_visible(timeout=5000)

    # Активация сотрудника
    page.get_by_role("gridcell", name=email).nth(1).click(button="right")
    page.get_by_role("link", name="Активировать", exact=True).click()
    page.get_by_role("button", name="Активировать").click()

    toast_activate = page.get_by_text("Сотрудник успешно активирован", exact=True)
    expect(toast_activate).to_be_visible(timeout=5000)
