import re
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize("login, password", [
    ("rodnischev@safib.ru", "1"),
])
def test_login_flow(page: Page, login, password):
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")
    page.get_by_role("textbox", name="Email или Логин").fill(login)
    page.get_by_role("textbox", name="Пароль").fill(password)
    page.get_by_role("button", name="Вход").click()
    expect(page).to_have_url(re.compile("http://lk.corp.dev.ru/ClientOrg"))
