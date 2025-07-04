import time
import pytest
from playwright.sync_api import Page, expect
from conftest import get_current_environment, ENVIRONMENTS

def test_activate_license_for_account(auth_page: Page, request):
    env = get_current_environment(request)
    config = ENVIRONMENTS[env]
    page = auth_page

    # Переход: Администрирование → Учетные записи
    page.get_by_role("link", name=" Администрирование ").click()
    time.sleep(1)
    page.get_by_role("link", name=" Учетные записи").click()
    time.sleep(1)

    # Поиск нужного аккаунта
    target_email = "rodnischev12@mailforspam.com"
    page.get_by_role("searchbox", name="Поиск:").fill(target_email)
    page.get_by_role("searchbox", name="Поиск:").press("Enter")
    time.sleep(2)

    # Контекстное меню → Активировать лицензию
    page.get_by_role("gridcell", name=target_email).click(button="right")
    page.get_by_role("link", name="Активировать лицензию").click()
    time.sleep(1)

    # Выбор лицензии "тест андрей"
    page.locator("div.SumoSelect.sumo_Text").click()
    time.sleep(0.5)
    page.locator("div.SumoSelect.sumo_Text ul.options label", has_text="тест андрей").click()
    time.sleep(0.5)

    # Активация лицензии
    page.get_by_role("button", name="Активировать", exact=True).click()
    expect(page.locator("div").filter(has_text="Лицензия успешно активирована").nth(1)).to_be_visible(timeout=5000)

    # Повторная активация через чекбокс
    page.get_by_role("row", name=f"Активен {target_email[:15]}").get_by_role("checkbox").check()
    page.get_by_role("button", name="Активировать лицензию").click()
    page.get_by_role("button", name="Активировать", exact=True).click()
    expect(page.locator("div").filter(has_text="Лицензия успешно активирована у выбранных учетных записей").nth(1)).to_be_visible(timeout=5000)
