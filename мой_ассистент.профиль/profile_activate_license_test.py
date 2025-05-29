import pytest
from playwright.sync_api import Page, expect

def toggle_registration_setting(page: Page):
    page.get_by_role("link", name="Администрирование").click()
    page.get_by_role("link", name="Системные настройки").click()
    page.locator("div:nth-child(3) > .col-sm-10 > .i-checks > .icheckbox_square-green > .iCheck-helper").first.click()
    page.get_by_role("button", name="Сохранить").click()

def test_activate_and_cancel_license(auth_page: Page):
    page = auth_page

    toggle_registration_setting(page)

    # Переход в профиль
    page.get_by_role("link", name="Мой ассистент").click()
    page.get_by_role("link", name=" Профиль").click()

    # Если уже активна лицензия "тест андрей", сначала отменим её
    if page.get_by_role("link", name="тест андрей").count() > 0:
        page.get_by_role("link", name="тест андрей").first.click()
        page.get_by_role("button", name="Активировать").click()
        expect(page.locator("div.toast-message", has_text="Лицензия отменена")).to_be_visible(timeout=5000)

    # Активируем базовую
    page.get_by_role("link", name="Активировать").first.click()
    page.locator("#Text").fill("CB71353D-619BEC40-8076D68A-FF302886")
    page.get_by_role("button", name="Активировать").click()
    expect(page.locator("div.toast-message", has_text="Лицензия успешно активирована")).to_be_visible(timeout=5000)

    # Активируем "тест андрей"
    page.get_by_role("link", name="тест андрей").first.click()
    page.get_by_role("button", name="Активировать").click()
    expect(page.locator("div.toast-message", has_text="Лицензия успешно активирована")).to_be_visible(timeout=5000)

    toggle_registration_setting(page)
