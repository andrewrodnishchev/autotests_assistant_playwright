import time
from playwright.sync_api import expect

def test_send_data_request(auth_page):
    page = auth_page

    # Переход в раздел "Устройства"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Отметка устройства и отправка команды
    page.get_by_role("row", name="  014 917 927 c405-Andrey2").get_by_role("checkbox").check()
    page.get_by_role("button", name="").click()
    page.get_by_role("button", name="Отправить").click()
    # Подтверждение сообщения
    page.locator("div").filter(has_text="Запросы успешно отправлены")

    # Клик ПКМ по устройству и отправка запроса на сбор данных
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Отправить запрос на сбор данных").click()
    page.get_by_role("button", name="Отправить").click()

    # Подтверждение второго сообщения
    page.locator("div").filter(has_text="Запрос успешно отправлен")
