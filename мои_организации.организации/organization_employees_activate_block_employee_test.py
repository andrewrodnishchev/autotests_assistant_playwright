import pytest
from playwright.sync_api import Page, expect

def test_block_and_activate_employee(auth_page: Page):
    """Блокировка и активация сотрудника."""
    page = auth_page

    # Переход в нужную организацию
    page.get_by_role("link", name="тест андрей").click()
    page.wait_for_timeout(500)

    page.get_by_role("link", name="Сотрудники").click()
    page.wait_for_timeout(500)

    # Блокировка сотрудника
    email = "rodnischev54321@mailforspam.com"
    page.get_by_role("gridcell", name=email).nth(1).click(button="right")
    page.wait_for_timeout(300)

    page.get_by_role("link", name="Заблокировать").click()
    page.wait_for_timeout(300)

    page.get_by_role("button", name="Заблокировать").click()
    page.wait_for_timeout(300)

    toast_block = page.get_by_text("Сотрудник успешно заблокирован", exact=True)
    expect(toast_block).to_be_visible(timeout=5000)
    page.wait_for_timeout(500)

    # Активация сотрудника
    page.get_by_role("gridcell", name=email).nth(1).click(button="right")
    page.wait_for_timeout(300)

    page.get_by_role("link", name="Активировать", exact=True).click()
    page.wait_for_timeout(300)

    page.get_by_role("button", name="Активировать").click()
    page.wait_for_timeout(300)

    toast_activate = page.get_by_text("Сотрудник успешно активирован", exact=True)
    expect(toast_activate).to_be_visible(timeout=5000)
    page.wait_for_timeout(500)
