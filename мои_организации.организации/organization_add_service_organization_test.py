import pytest
from playwright.sync_api import Page, expect
from conftest import ENVIRONMENTS, get_current_environment


def login(page: Page, base_url: str, email: str, password: str):
    login_url = f"{base_url}/Account/Login?returnUrl=%2FClientOrg"
    page.goto(login_url)

    locator = page.get_by_role("textbox", name="Email или Логин")
    if not locator.is_visible(timeout=2000):
        locator = page.get_by_role("textbox", name="Email")
    locator.fill(email)

    page.get_by_role("textbox", name="Пароль").fill(password)
    page.get_by_role("button", name="Вход").click()
    expect(page).not_to_have_url(login_url, timeout=5000)


@pytest.mark.usefixtures("page")
def test_create_and_delete_organization_with_extra_click(page: Page, request):
    # Получаем URL текущего окружения
    env = get_current_environment(request)
    config = ENVIRONMENTS[env]
    base_url = config["base_url"]

    # Используем конкретного пользователя, независимо от --env
    login_email = "test@safib.ru"
    password = "1"

    # Логинимся
    login(page, base_url, login_email, password)

    # Создание организации
    page.get_by_role("link", name="Добавить организацию").click()
    page.locator("#Name").click()
    page.locator("#Name").fill("тест ар сервис")

    # Дополнительный клик по области или другому элементу
    page.get_by_role("insertion").nth(1).click()

    # Сохранение
    page.get_by_role("button", name="Сохранить").click()

    # Проверка создания
    expect(
        page.locator("div").filter(has_text="Организация успешно создана").nth(1)
    ).to_be_visible(timeout=5000)

    # Удаление
    page.get_by_role("link", name="Изменить").click()
    page.get_by_role("link", name="Удалить организацию").click()
    page.get_by_role("button", name="Удалить").click()

    # Проверка удаления
    expect(
        page.locator("div").filter(has_text="Организация удалена").nth(1)
    ).to_be_visible(timeout=5000)
