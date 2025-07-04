import pytest
import time
from playwright.sync_api import sync_playwright, expect

# Вспомогательная функция — получаем base_url из conftest по --env
def get_base_url(request: pytest.FixtureRequest) -> str:
    env = request.config.getoption("--env")
    from conftest import ENVIRONMENTS  # импорт из твоего conftest
    return ENVIRONMENTS[env]["base_url"]

@pytest.mark.environment("corp")  # можно указать любое окружение по умолчанию
def test_keycloak_username_change_and_login(request):
    base_url = get_base_url(request)

    with sync_playwright() as playwright:
        # Сессия 1: Админ меняет имя пользователя в Keycloak
        browser1 = playwright.chromium.launch(headless=False)
        context1 = browser1.new_context(viewport={"width": 1920, "height": 1080})
        page1 = context1.new_page()

        page1.goto("https://keycloak.safib.ru:8443")
        page1.get_by_role("textbox", name="Username or email").fill("admin")
        page1.get_by_role("textbox", name="Password").fill("nimda")
        page1.get_by_role("button", name="Sign In").click()
        time.sleep(2)

        page1.get_by_test_id("nav-item-users").click()
        time.sleep(1)
        page1.get_by_role("link", name="andreyr").click()
        time.sleep(1)
        page1.get_by_test_id("firstName").fill("andrey")
        page1.get_by_test_id("lastName").fill("rodnischev")
        page1.get_by_role("button", name="Save").click()
        time.sleep(2)

        context1.close()
        browser1.close()

        # Сессия 2: Пользователь логинится через Keycloak
        browser2 = playwright.chromium.launch(headless=False)
        context2 = browser2.new_context(viewport={"width": 1920, "height": 1080})
        page2 = context2.new_page()

        page2.goto(f"{base_url}/Account/Login?returnUrl=%2FClientOrg")
        page2.get_by_role("link", name="Вход через Keycloak").click()
        time.sleep(2)

        # Keycloak-авторизация
        page2_auth = context2.new_page()
        page2_auth.goto("https://keycloak.safib.ru:8443")
        # После авторизации на Keycloak:
        page2_auth.get_by_role("textbox", name="Username or email").fill("testast1@mailforspam.com")
        page2_auth.get_by_role("textbox", name="Password").fill("1")
        page2_auth.get_by_role("button", name="Sign In").click()
        time.sleep(3)

        # ✅ теперь переключаемся обратно на page2 — он должен обновиться после авторизации
        page2.bring_to_front()  # Поднимаем вкладку
        expect(page2.locator("span.uname", has_text="andrey rodnischev")).to_be_visible(timeout=5000)
        page2.locator("span.uname", has_text="andrey rodnischev").click()

        time.sleep(2)


        context2.close()
        browser2.close()

        # Сессия 3: Админ сбрасывает ФИО пользователя
        browser3 = playwright.chromium.launch(headless=False)
        context3 = browser3.new_context(viewport={"width": 1920, "height": 1080})
        page3 = context3.new_page()

        page3.goto("https://keycloak.safib.ru:8443")
        page3.get_by_role("textbox", name="Username or email").fill("admin")
        page3.get_by_role("textbox", name="Password").fill("nimda")
        page3.get_by_role("button", name="Sign In").click()
        time.sleep(2)

        page3.get_by_test_id("nav-item-users").click()
        time.sleep(1)
        page3.get_by_role("link", name="andreyr").click()
        time.sleep(1)
        page3.get_by_test_id("firstName").fill("")
        page3.get_by_test_id("lastName").fill("")
        page3.get_by_role("button", name="Save").click()
        time.sleep(2)

        context3.close()
        browser3.close()
