import pytest
from playwright.sync_api import expect


def test_activate_license_for_device(auth_page):
    page = auth_page

    # Переход на "тест андрей"
    page.get_by_role("link", name="тест андрей").click()

    # Открытие вкладки "Устройства"
    page.get_by_role("link", name="Устройства").click()

    # ПКМ по устройству "026 892"
    page.get_by_role("gridcell", name="135 026 892").click(button="right")

    # Нажатие "Активировать лицензию"
    page.get_by_role("link", name="Активировать лицензию").click()

    # Кликаем по селекту "Деактивировать лицензию"
    license_select = page.locator(".SumoSelect", has=page.locator(".CaptionCont", has_text="По умолчанию"))
    license_select.click()


    # Ищем конкретную опцию *внутри* этого селекта
    option = license_select.locator(".opt label", has_text="тест андрей")
    expect(option).to_have_count(1, timeout=5000)  # контроль, что найден только один
    option.click()

    page.get_by_role("button", name="Активировать").click()


    # Проверка уведомления
    success_banner = page.locator("div").filter(has_text="Лицензия успешно активирована")
    expect(success_banner.first).to_be_visible(timeout=5000)

    # Активация через чекбокс (добавленная часть)

    row = page.get_by_role("row", name="135 026 892")
    row.get_by_role("checkbox").check()

    page.get_by_role("button", name="").click()
    page.wait_for_timeout(500)  # маленькая пауза, можно убрать если не требуется


    # Нажатие на кнопку "Активировать"
    page.get_by_role("button", name="Активировать").click()

    # Проверка уведомления
    toast = page.locator("#toast-container").get_by_text("Лицензия успешно активирована на выбранных устройствах (1 шт.)")
    expect(toast).to_be_visible(timeout=5000)

