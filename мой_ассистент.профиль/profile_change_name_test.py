import pytest
from playwright.sync_api import Page, expect


def test_change_and_revert_name(auth_page: Page):
    page = auth_page

    # Переход в профиль
    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Профиль").click()
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
