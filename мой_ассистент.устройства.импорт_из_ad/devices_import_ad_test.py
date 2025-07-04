import pytest
from playwright.sync_api import expect
import time


@pytest.mark.parametrize("device_number", ["051 238 713"])
def test_import_and_delete_device_from_ad(auth_page, device_number):
    page = auth_page
    timeout = 10_000
    toast_import_success = "Успешно импортировано/обновлено 1 устройство"
    toast_delete_success = "Устройство удалено"

    # Переход к разделу "Устройства"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Открытие формы подключения к AD
    page.get_by_role("link", name="").click()

    # Заполнение данных подключения
    page.locator("#ServerName").fill("dc01.test.local")
    page.locator("#UN").fill("user1")
    page.locator("#Pwd").fill("123")
    page.locator("#BaseDN").fill("dc=test,dc=local")

    # Подключение
    page.get_by_role("button", name="Подключиться").click()
    time.sleep(10)
    # Переход к импорту устройств
    #page.goto("http://lk.corp.dev.ru/ClientOrg/ImportFromAD")

    # Поиск устройства
    page.get_by_role("searchbox", name="Поиск:").fill(device_number)
    page.get_by_role("searchbox", name="Поиск:").press("Enter")

    # Подождать, пока появится строка устройства (может занять время)
    page.wait_for_timeout(2000)

    # Выбор устройства
    checkbox = page.get_by_role("row", name=f"{device_number}").get_by_role("checkbox")
    checkbox.click()

    # Импорт устройства
    page.get_by_role("button", name="Импортировать в организацию").click()
    page.get_by_role("insertion").first.click()
    page.get_by_role("button", name="Выполнить").click()
    time.sleep(3)

    # Долгая загрузка после нажатия "Выполнить"
    time.sleep(5)

    # Повторный переход для загрузки списка устройств
    #page.goto("http://lk.corp.dev.ru/ClientOrg/ImportFromAD")

    # Проверка тоста об успешном импорте
    toast = page.locator("div").filter(has_text=toast_import_success).nth(1)
    toast.wait_for(timeout=timeout)
    toast.click()

    # Переход к разделу устройств
    page.get_by_role("link", name="Устройства").click()
    page.wait_for_timeout(2000)

    # Удаление устройства
    page.get_by_role("gridcell", name=device_number.split()[1]).click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_role("button", name="Удалить").click()

    # Подождать, пока появится уведомление
    page.wait_for_timeout(2000)

    # Проверка тоста об удалении
    toast = page.locator("div").filter(has_text=toast_delete_success).nth(1)
    toast.wait_for(timeout=timeout)
    toast.click()
