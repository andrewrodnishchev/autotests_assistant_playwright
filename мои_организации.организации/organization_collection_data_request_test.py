import pytest
from playwright.sync_api import expect

def test_data_collection_request(auth_page):
    page = auth_page

    # Навигация к нужному устройству
    page.get_by_role("link", name="тест андрей").click()
    page.wait_for_timeout(500)

    page.get_by_role("link", name="Устройства").click()
    page.wait_for_timeout(500)
    page.get_by_role("row", name="  014 917 927 c405-Andrey").get_by_role("checkbox").check()
    page.get_by_role("button", name="").click()
    page.wait_for_timeout(500)
    # Клик на кастомный селект, чтобы открыть список
    page.locator("div.SumoSelect.sumo_InventoryPoliticId").click()
    page.wait_for_timeout(500)
    # Явно выбрать нужный пункт из списка по тексту "тест"
    page.locator("div.SumoSelect.sumo_InventoryPoliticId ul.options li.opt label", has_text="тест").click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Сохранить").click()
    page.wait_for_timeout(500)
    page.locator("div").filter(has_text="Устройство успешно сохранено").nth(1).click()
    page.get_by_role("link", name="Назад").click()

    page.get_by_role("link", name="Коллекции").click()
    page.wait_for_timeout(500)

    # Найти строку с "информация об устройстве"
    row = page.locator("tr", has=page.get_by_text("информация об устройстве"))
    page.wait_for_timeout(500)

    # Кликнуть правой кнопкой по этой строке (если нужно)
    row.click(button="right")
    page.wait_for_timeout(300)

    # В этой строке найти ссылку "Синхронизировать" и кликнуть по ней
    sync_button = row.locator("a", has_text="Синхронизировать")
    sync_button.click()
    page.wait_for_timeout(1000)

    # Отправка запроса на сбор данных для одного устройства
    page.get_by_role("gridcell", name="014 917 927").click(button="right")
    page.wait_for_timeout(300)

    page.get_by_role("link", name="Собрать инвентаризацию").click()
    page.wait_for_timeout(300)

    page.get_by_role("button", name="Отправить").click()
    page.wait_for_timeout(500)

    # Проверка сообщения об успешной отправке
    expect(page.locator("div.toast-message", has_text="Отправлен запрос сбора инвентаризации с устройств.")).to_be_visible(timeout=5000)
    page.wait_for_timeout(500)

    # Массовая отправка (через чекбокс и кнопку)
    # Найти строку, где есть нужный идентификатор устройства
    row = page.locator("tr", has_text="014 917 927")
    # Найти в этой строке checkbox и кликнуть по нему
    page.wait_for_timeout(500)

    page.locator("tr#580725 input.js-chk[type='checkbox']").click()



    page.get_by_role("button", name="").click()  # кнопка с иконкой
    page.wait_for_timeout(300)

    page.get_by_role("button", name="Отправить").click()
    page.wait_for_timeout(500)
