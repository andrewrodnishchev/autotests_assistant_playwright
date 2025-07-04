import pytest
from playwright.sync_api import expect

def test_change_time_zone(auth_page):
    page = auth_page

    # Переход в профиль
    page.get_by_role("link", name="Андрей Роднищев").click()
    page.get_by_role("link", name="Профиль").click()

    # Выбор часового пояса UTC+03:00 и сохранение
    page.get_by_role("link", name="(UTC+03:00").click()
    page.locator("#TimeZoneId").select_option("49")
    page.get_by_role("button", name="Сохранить").click()
    page.locator("div").filter(has_text="Часовой пояс успешно изменен").nth(1).click()

    # Смена на UTC+00:00 и сохранение
    page.get_by_role("link", name="(UTC+00:00").click()
    page.locator("#TimeZoneId").select_option("71")
    page.get_by_role("button", name="Сохранить").click()
    page.locator("div").filter(has_text="Часовой пояс успешно изменен").nth(1).click()
