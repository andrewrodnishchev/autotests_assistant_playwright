import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize("login, password", [
    ("rodnischev@safib.ru", "2"),
])
def test_unsuccessful_login_shows_error_message(page: Page, login, password):
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")
    page.get_by_role("textbox", name="Email или Логин").fill(login)
    page.get_by_role("textbox", name="Пароль").fill(password)
    page.get_by_role("button", name="Вход").click()
    expect(page.get_by_text("Неверно указан логин или пароль")).to_be_visible()
