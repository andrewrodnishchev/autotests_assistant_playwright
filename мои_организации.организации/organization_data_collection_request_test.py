import time
from playwright.sync_api import expect

def test_send_data_request(auth_page):
    page = auth_page

    # Переход в раздел "Устройства"
    page.get_by_role("link", name="тест андрей").click()
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Устройства").click()
    page.wait_for_timeout(500)

    # Отметка устройства и отправка команды
    page.get_by_role("row", name="014 917 927").get_by_role("checkbox").check()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="").click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Отправить").click()
    page.wait_for_timeout(500)
    # Подтверждение сообщения
    page.locator("div").filter(has_text="Отправлен запрос сбора инвентаризации с устройств: 1.")

    page.wait_for_timeout(500)
    # Клик ПКМ по устройству и отправка запроса на сбор данных
    page.get_by_role("gridcell", name="014 917 927").click(button="right")
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Собрать инвентаризацию").click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Отправить").click()
    page.wait_for_timeout(500)

    # Подтверждение второго сообщения
    page.locator("div").filter(has_text="Отправлен запрос сбора инвентаризации с устройств.")
