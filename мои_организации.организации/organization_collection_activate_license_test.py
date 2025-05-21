import pytest
from playwright.sync_api import Page, expect


def test_activate_license(auth_page: Page):
    page = auth_page

    # Переход к устройствам
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Коллекции").click()
    page.get_by_text("информация об устройстве").click()

    # Правый клик по устройству
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Активировать лицензию").click()

    # Выбор лицензии (два шага: шаблон и организация)
    page.get_by_role("button", name="По умолчанию1").click()
    page.get_by_role("button", name="тест андрей").click(force=True)

    # Активация
    page.get_by_role("button", name="Активировать").click(force=True)
    page.get_by_role("button", name="Активировать").click(force=True)

    expect(page.locator("div.toast-message", has_text="Лицензия успешно активирована")).to_be_visible(timeout=5000)


    # Массовая активация
    page.get_by_role("checkbox").check()
    page.get_by_role("button", name="").click()
    page.get_by_role("button", name="Активировать").click()
    page.locator("div").filter(has_text="Лицензия успешно активирована для 1 устройств").nth(1).wait_for(timeout=5000)
