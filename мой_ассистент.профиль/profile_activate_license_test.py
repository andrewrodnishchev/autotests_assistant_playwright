import pytest
from playwright.sync_api import Page, expect

def ensure_checkbox_checked(page: Page):
    checkbox_input = page.locator("input#IsSelfRegistrationAveeble")
    is_checked = checkbox_input.evaluate("el => el.checked")
    if not is_checked:
        page.locator("input#IsSelfRegistrationAveeble + ins.iCheck-helper").click()
        page.wait_for_timeout(500)

def ensure_checkbox_unchecked(page: Page):
    checkbox_input = page.locator("input#IsSelfRegistrationAveeble")
    is_checked = checkbox_input.evaluate("el => el.checked")
    if is_checked:
        page.locator("input#IsSelfRegistrationAveeble + ins.iCheck-helper").click()
        page.wait_for_timeout(500)

def enable_registration_setting(page: Page):
    page.get_by_role("link", name="Администрирование").click()
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Системные настройки").click()
    page.wait_for_timeout(1000)
    ensure_checkbox_checked(page)
    page.get_by_role("button", name="Сохранить").click()
    page.wait_for_timeout(1000)

def disable_registration_setting(page: Page):
    page.get_by_role("link", name="Администрирование").click()
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Системные настройки").click()
    page.wait_for_timeout(1000)
    ensure_checkbox_unchecked(page)
    page.get_by_role("button", name="Сохранить").click()
    page.wait_for_timeout(1000)

def test_activate_and_cancel_license(auth_page: Page):
    page = auth_page

    enable_registration_setting(page)

    # Переход в профиль
    page.get_by_role("link", name="Мой ассистент").click()
    page.wait_for_timeout(500)
    page.get_by_role("link", name=" Профиль").click()
    page.wait_for_timeout(1000)

    # Если уже активна лицензия "тест андрей", сначала отменим её
    if page.get_by_role("link", name="тест андрей").count() > 0:
        page.get_by_role("link", name="тест андрей").first.click()
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Активировать").click()
        page.wait_for_timeout(1000)
        expect(page.locator("div.toast-message", has_text="Лицензия отменена")).to_be_visible(timeout=5000)
        page.wait_for_timeout(1000)

    # Активируем базовую
    page.get_by_role("link", name="Активировать").first.click()
    page.wait_for_timeout(500)
    page.locator("#Text").fill("CB71353D-619BEC40-8076D68A-FF302886")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Активировать").click()
    page.wait_for_timeout(1000)
    expect(page.locator("div.toast-message", has_text="Лицензия успешно активирована")).to_be_visible(timeout=5000)
    page.wait_for_timeout(1000)

    # Активируем "тест андрей"
    page.get_by_role("link", name="тест андрей").first.click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Активировать").click()
    page.wait_for_timeout(1000)
    expect(page.locator("div.toast-message", has_text="Лицензия отменена")).to_be_visible(timeout=5000)
    page.wait_for_timeout(1000)

    disable_registration_setting(page)
