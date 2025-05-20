import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize("license_key", ["CB71353D-619BEC40-8076D68A-FF302886"])
def test_activate_and_cancel_license(auth_page: Page, license_key: str):
    page = auth_page

    # Переход в раздел профиля → активация лицензии
    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Профиль").click()
    page.get_by_role("link", name="Активировать").click()

    # Ввод ключа и активация
    page.locator("#Text").fill(license_key)
    page.get_by_role("button", name="Активировать").click()

    # Проверка сообщения об успешной активации
    expect(page.locator("div.toast-message", has_text="Лицензия успешно активирована")).to_be_visible(timeout=5000)

    # Переход к пользователю "тест андрей"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("button", name="Активировать").click()

    # Проверка сообщения об отмене лицензии
    expect(page.locator("div.toast-message", has_text="Лицензия отменена")).to_be_visible(timeout=5000)
