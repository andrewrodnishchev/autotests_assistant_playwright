import pytest
from playwright.sync_api import expect

def test_data_collection_request(auth_page):
    page = auth_page

    # Навигация к нужному устройству
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Коллекции").click()
    page.get_by_text("информация об устройстве").click()

    # Отправка запроса на сбор данных для одного устройства
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Отправить запрос на сбор данных").click()
    page.get_by_role("button", name="Отправить").click()

    # Проверка сообщения об успешной отправке
    expect(page.locator("div.toast-message", has_text="Запрос успешно отправлен")).to_be_visible()

    # Массовая отправка (через чекбокс и кнопку)
    page.get_by_role("checkbox").check()
    page.get_by_role("button", name="").click()  # кнопка с иконкой
    page.get_by_role("button", name="Отправить").click()