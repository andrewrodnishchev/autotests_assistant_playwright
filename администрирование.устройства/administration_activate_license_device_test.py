import pytest
from playwright.sync_api import expect

def test_activate_license(auth_page):
    page = auth_page

    # Переход в Администрирование > Устройства
    page.get_by_role("link", name=" Администрирование ").click()
    page.get_by_role("link", name=" Устройства").click()

    # Поиск устройства по номеру
    searchbox = page.get_by_role("searchbox", name="Поиск:")
    searchbox.click()
    searchbox.fill("135 026 892")
    searchbox.press("Enter")

    # --- Первая активация ---

    # Правый клик по устройству
    page.get_by_role("gridcell", name="026 892").click(button="right")

    # Клик "Активировать лицензию"
    page.get_by_role("link", name="Активировать лицензию").click()

    # Открываем кастомный селект и выбираем нужную опцию
    dropdown = page.locator("div.SumoSelect.sumo_Text")
    dropdown.click()
    option = page.locator("ul.options li.opt label", has_text="тест андрей CB71353D-619BEC40-8076D68A-FF302886")
    option.click()

    # Жмём кнопку "Активировать"
    page.get_by_role("button", name="Активировать", exact=True).click()

    # Проверяем успешную активацию
    expect(page.locator("div", has_text="Лицензия успешно активирована").nth(1)).to_be_visible(timeout=5000)

    # --- Вторая активация ---

    # Снова правый клик по устройству
    page.get_by_role("gridcell", name="026 892").click(button="right")

    # Клик "Активировать лицензию"
    page.get_by_role("link", name="Активировать лицензию").click()

    # Во второй активации НЕ выбираем опцию, просто сразу жмём "Активировать"
    page.get_by_role("button", name="Активировать", exact=True).click()

    # Проверяем успешную активацию второй лицензии
    expect(page.locator("div", has_text="Лицензия успешно активирована").nth(1)).to_be_visible(timeout=5000)
