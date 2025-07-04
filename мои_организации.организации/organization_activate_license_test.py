import pytest
from playwright.sync_api import expect

def test_activate_license_for_device(auth_page):
    page = auth_page

    # Переход на "тест андрей"
    page.get_by_role("link", name="тест андрей").click()
    page.wait_for_timeout(1000)

    # Открытие вкладки "Устройства"
    page.get_by_role("link", name="Устройства").click()
    page.wait_for_timeout(1000)

    # ПКМ по устройству "014 917 927"
    page.get_by_role("gridcell", name="014 917 927").click(button="right")
    page.wait_for_timeout(500)

    # Нажатие "Активировать лицензию"
    page.get_by_role("link", name="Активировать лицензию").click()
    page.wait_for_timeout(1000)

    # Кликаем по селекту "По умолчанию"
    license_select = page.locator(".SumoSelect", has=page.locator(".CaptionCont", has_text="По умолчанию"))
    license_select.click()
    page.wait_for_timeout(500)

    # Ищем и кликаем по опции "тест андрей"
    option = license_select.locator(".opt label", has_text="тест андрей")
    expect(option).to_have_count(1, timeout=5000)
    option.click()
    page.wait_for_timeout(500)

    # Кнопка "Активировать"
    page.get_by_role("button", name="Активировать").click()
    page.wait_for_timeout(1000)

    # Проверка уведомления
    success_banner = page.locator("div", has_text="Лицензия успешно активирована").first
    already_active_banner = page.locator("div", has_text="Лицензия уже активирована на выбранном устройстве").first
    expect(success_banner.or_(already_active_banner)).to_be_visible(timeout=5000)

    # --- Активация через чекбокс ---
    row = page.get_by_role("row", name="014 917 927")
    row.get_by_role("checkbox").check()
    page.wait_for_timeout(500)

    page.get_by_role("button", name="").click()
    page.wait_for_timeout(1000)

    page.get_by_role("button", name="Активировать").click()
    page.wait_for_timeout(1000)

    # Проверка уведомления
    toast = page.locator("#toast-container").get_by_text(
        "Лицензия успешно активирована на выбранных устройствах (1 шт.)"
    )
    expect(toast).to_be_visible(timeout=5000)
