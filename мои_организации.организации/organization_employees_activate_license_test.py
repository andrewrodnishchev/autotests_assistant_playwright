import pytest
from playwright.sync_api import expect

def test_deactivate_and_activate_license(auth_page):
    page = auth_page

    # Переход в раздел "Сотрудники"
    page.get_by_role("link", name="тест андрей").click()
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Сотрудники").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    # Выбор сотрудника
    email = "rodnischev54321@mailforspam."
    row = page.get_by_role("row", name=email)
    row.get_by_role("checkbox").check()
    page.wait_for_timeout(500)

    # Нажимаем на кнопку "ключ"
    page.get_by_role("button", name="").click()
    page.wait_for_timeout(1000)

    # Кликаем по селекту "Деактивировать лицензию"
    license_select = page.locator(".SumoSelect", has=page.locator(".CaptionCont", has_text="Деактивировать лицензию"))
    license_select.click()
    page.wait_for_timeout(500)

    # Ищем конкретную опцию *внутри* этого селекта
    option = license_select.locator(".opt label", has_text="тест андрей")
    expect(option).to_have_count(1, timeout=5000)
    option.click()
    page.wait_for_timeout(500)

    # Нажимаем кнопку "Выполнить"
    page.get_by_role("button", name="Выполнить").click()
    page.wait_for_timeout(1000)

    # Проверка уведомления об успешной деактивации
    success_banner = page.locator("div").filter(has_text="Успешно изменено сотрудников:")
    expect(success_banner.first).to_be_visible(timeout=5000)
    page.wait_for_timeout(500)

    # Активация лицензии
    page.get_by_role("gridcell", name=email).first.click(button="right")
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Активировать лицензию").click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Активировать").click()
    page.wait_for_timeout(1000)

    # Проверка уведомления об отмене лицензии
    license_banner = page.locator("div").filter(has_text="Лицензия отменена")
    expect(license_banner.first).to_be_visible(timeout=5000)
