import pytest
from playwright.sync_api import Page, expect

@pytest.mark.usefixtures("page")
def test_create_and_delete_organization_simple(page: Page):
    # Авторизация
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")
    page.get_by_role("textbox", name="Email или Логин").fill("test@safib.ru")
    page.get_by_role("textbox", name="Пароль").fill("1")
    page.get_by_role("button", name="Вход").click()

    # Создание организации
    page.get_by_role("link", name="Добавить организацию").click()
    page.locator("#Name").click()
    page.locator("#Name").fill("тест ар")
    page.get_by_role("button", name="Сохранить").click()

    expect(
        page.locator("div").filter(has_text="Организация успешно создана").nth(1)
    ).to_be_visible(timeout=5000)

    # Удаление организации
    page.get_by_role("link", name="Изменить").click()
    page.get_by_role("link", name="Удалить организацию").click()
    page.get_by_role("button", name="Удалить").click()

    expect(
        page.locator("div").filter(has_text="Организация удалена").nth(1)
    ).to_be_visible(timeout=5000)
