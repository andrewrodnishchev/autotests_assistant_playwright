import pytest
from playwright.sync_api import Page, expect
import time


def test_activate_license(auth_page: Page):
    page = auth_page

    # Переход к устройствам
    page.get_by_role("link", name="тест андрей").click()
    page.wait_for_timeout(500)

    page.get_by_role("link", name="Коллекции").click()
    page.wait_for_timeout(500)

    page.get_by_text("информация об устройстве").click(button="right")
    page.wait_for_timeout(300)

    # Ждём появления нужной кнопки синхронизации именно для этой строки
    target_sync = page.locator('a.js-btngrid[href*="collectionId=23"]', has_text="Синхронизировать")
    target_sync.wait_for(state="visible", timeout=3000)

    # Кликаем по нужному элементу
    target_sync.click()
    time.sleep(3)
    # Правый клик по устройству
    page.get_by_role("gridcell", name="014 917 927").click(button="right")
    page.wait_for_timeout(500)

    page.get_by_role("link", name="Активировать лицензию").click()
    page.wait_for_timeout(500)

    # Выбор лицензии (два шага: шаблон и организация)
    page.get_by_role("button", name="По умолчанию").click()
    page.wait_for_timeout(300)

    page.locator("li.opt label", has_text="тест андрей CB71353D-619BEC40-8076D68A-FF302886").click()
    page.wait_for_timeout(300)

    # Активация
    page.get_by_role("button", name="Активировать").click(force=True)
    page.get_by_role("button", name="Активировать").click(force=True)
    page.wait_for_timeout(300)

    expect(page.locator("div.toast-message", has_text="Лицензия успешно активирована")).to_be_visible(timeout=5000)
    page.wait_for_timeout(1000)

    # Найти строку, где есть нужный идентификатор устройства
    row = page.locator("tr", has_text="014 917 927")
    # Найти в этой строке checkbox и кликнуть по нему
    row.locator("input.js-chk[type='checkbox']").click()

    page.wait_for_timeout(300)

    page.get_by_role("button", name="").click()
    page.wait_for_timeout(300)

    page.get_by_role("button", name="Активировать").click()
    page.locator("div").filter(has_text="Лицензия успешно активирована для 1 устройств").nth(1).wait_for(timeout=5000)
