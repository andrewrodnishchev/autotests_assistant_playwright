import pytest
from playwright.sync_api import Page, expect

ADMIN_EMAIL = "rodnischev@safib.ru"
ADMIN_PASSWORD = "1"

USER_EMAIL = "ast123@mailforspam.com"
USER_PASSWORD = "1"

def login(page: Page, email: str, password: str):
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")
    page.get_by_role("textbox", name="Email или Логин").fill(email)
    page.get_by_role("textbox", name="Пароль").fill(password)
    page.get_by_role("button", name="Вход").click()
    page.wait_for_load_state("networkidle")

def logout(page: Page):
    try:
        page.get_by_role("link", name="Выход").wait_for(state="visible", timeout=10000)
        page.get_by_role("link", name="Выход").click()
    except Exception:
        print("Не удалось найти ссылку Выход, пропускаем logout")

def toggle_checkbox_in_system_settings(page: Page):
    page.get_by_role("link", name="Администрирование").click()
    page.get_by_role("link", name="Системные настройки").click()
    page.wait_for_load_state("networkidle")
    checkbox_locator = page.locator("div:nth-child(3) > .col-sm-10 > .i-checks > .icheckbox_square-green > .iCheck-helper").first
    checkbox_locator.click()
    page.get_by_role("button", name="Сохранить").click()
    # Можно добавить проверку уведомления об успешном сохранении, если есть

@pytest.mark.usefixtures("page")
def test_admin_toggle_checkbox_and_change_name(page: Page):
    # Вход под админом и включение чекбокса
    login(page, ADMIN_EMAIL, ADMIN_PASSWORD)
    toggle_checkbox_in_system_settings(page)
    logout(page)

    # Вход под обычным пользователем и смена имени
    login(page, USER_EMAIL, USER_PASSWORD)

    # Переход в профиль
    page.get_by_role("link", name="Мой ассистент").click()
    page.get_by_role("link", name="Профиль").click()
    page.wait_for_load_state("networkidle")

    # Смена имени: "Андрей Роднищев" → "андрей роднищев"
    page.locator("#tab-1").get_by_role("link", name="Андрей Роднищев").click()
    page.locator("#Name").fill("андрей роднищев")
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div.toast-message", has_text="Имя успешно изменено")).to_be_visible(timeout=5000)

    # Проверка: имя изменилось
    page.locator("#tab-1").get_by_role("link", name="андрей роднищев").click()
    assert page.locator("#Name").input_value() == "андрей роднищев"

    # Возврат имени обратно: "андрей роднищев" → "Андрей Роднищев"
    page.locator("#Name").fill("Андрей Роднищев")
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div.toast-message", has_text="Имя успешно изменено")).to_be_visible(timeout=5000)

    # Проверка: имя вернулось
    page.locator("#tab-1").get_by_role("link", name="Андрей Роднищев").click()
    assert page.locator("#Name").input_value() == "Андрей Роднищев"

    logout(page)

    # Вход под админом и выключение чекбокса
    login(page, ADMIN_EMAIL, ADMIN_PASSWORD)
    toggle_checkbox_in_system_settings(page)
    logout(page)
