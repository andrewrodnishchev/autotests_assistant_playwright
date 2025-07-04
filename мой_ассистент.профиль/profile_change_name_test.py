import pytest
import time
from playwright.sync_api import Page
from conftest import ENVIRONMENTS, get_current_environment

ADMIN_EMAIL = "rodnischev@safib.ru"
ADMIN_PASSWORD = "1"

USER_EMAIL = "ast123@mailforspam.com"
USER_PASSWORD = "1"

def login(page: Page, base_url: str, email: str, password: str):
    login_url = f"{base_url}/Account/Login?returnUrl=%2FClientOrg"
    page.goto(login_url)
    time.sleep(0.5)
    page.get_by_role("textbox", name="Email или Логин").fill(email)
    page.get_by_role("textbox", name="Пароль").fill(password)
    time.sleep(0.5)
    page.get_by_role("button", name="Вход").click()
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)

def logout(page: Page):
    try:
        page.get_by_role("link", name="Выход").wait_for(state="visible", timeout=10000)
        time.sleep(0.5)
        page.get_by_role("link", name="Выход").click()
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
    except Exception:
        pass

def toggle_checkbox_in_system_settings(page: Page, enable: bool):
    time.sleep(0.5)
    page.get_by_role("link", name="Администрирование").click()
    time.sleep(0.5)

    page.get_by_role("link", name="Системные настройки").click()
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)

    checkbox_input = page.locator("input#IsSelfRegistrationAveeble")
    is_checked = checkbox_input.is_checked()

    if is_checked != enable:
        checkbox_clickable = page.locator("div:nth-child(3) > .col-sm-10 > .i-checks > .icheckbox_square-green > .iCheck-helper").first
        time.sleep(0.5)
        checkbox_clickable.click()
        time.sleep(0.5)

    time.sleep(0.5)
    page.get_by_role("button", name="Сохранить").click()
    time.sleep(0.5)

@pytest.mark.usefixtures("page")
def test_admin_toggle_checkbox_and_change_name(page: Page, request):
    env = get_current_environment(request)
    config = ENVIRONMENTS[env]
    base_url = config["base_url"]

    login(page, base_url, ADMIN_EMAIL, ADMIN_PASSWORD)
    toggle_checkbox_in_system_settings(page, enable=True)
    logout(page)

    login(page, base_url, USER_EMAIL, USER_PASSWORD)
    time.sleep(0.5)

    page.get_by_role("link", name="Мой ассистент").click()
    time.sleep(0.5)

    page.get_by_role("link", name="Профиль").click()
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)

    page.locator("#tab-1").get_by_role("link", name="Андрей Роднищев").click()
    time.sleep(0.5)

    page.locator("#Name").fill("андрей роднищев")
    time.sleep(0.5)
    page.get_by_role("button", name="Сохранить").click()
    time.sleep(0.5)

    page.locator("#tab-1").get_by_role("link", name="андрей роднищев").click()
    time.sleep(0.5)
    assert page.locator("#Name").input_value() == "андрей роднищев"

    page.locator("#Name").fill("Андрей Роднищев")
    time.sleep(0.5)
    page.get_by_role("button", name="Сохранить").click()
    time.sleep(0.5)

    page.locator("#tab-1").get_by_role("link", name="Андрей Роднищев").click()
    time.sleep(0.5)
    assert page.locator("#Name").input_value() == "Андрей Роднищев"

    logout(page)

    login(page, base_url, ADMIN_EMAIL, ADMIN_PASSWORD)
    toggle_checkbox_in_system_settings(page, enable=False)
    logout(page)
