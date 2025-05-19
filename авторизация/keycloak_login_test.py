import pytest
from playwright.sync_api import Page, expect


@pytest.mark.usefixtures("page")
def test_keycloak_login(page: Page):
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")

    # Клик по ссылке входа через Keycloak
    page.get_by_role("link", name="Вход через Keycloak").click()

    # Заполнение логина и пароля
    page.get_by_role("textbox", name="Username or email").fill("ast1122@mailforspam.com")
    page.get_by_role("textbox", name="Password").fill("1")

    # Клик по кнопке Sign In
    page.get_by_role("button", name="Sign In").click()

    # Проверяем переход на нужную страницу
    expect(page).to_have_url("http://lk.corp.dev.ru/ClientOrg", timeout=10000)
