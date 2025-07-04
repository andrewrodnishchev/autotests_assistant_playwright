import pytest
import time
from playwright.sync_api import expect


@pytest.mark.parametrize("device_number", ["037 194 263"])
def test_import_and_delete_device_from_ipa(auth_page, device_number):
    page = auth_page
    timeout = 10_000
    toast_import_success = "Успешно импортировано/обновлено 1 устройство"
    toast_delete_success = "Устройство удалено"

    # Переход к разделу "Устройства"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Открытие формы подключения
    page.get_by_role("link", name="").click()

    # Выбор "IPA" в обычном <select>
    page.locator("select#ADSystem").select_option("FreeIPA")
    time.sleep(0.5)


    # Заполнение данных подключения к IPA
    page.locator("#ServerName").fill("192.168.71.76")
    page.locator("#UN").fill("uid=savenko,cn=users,cn=accounts,dc=ipa,dc=local")
    page.locator("#Pwd").fill("12345678")
    page.locator("#BaseDN").fill("dc=ipa,dc=local")

    # Подключение
    page.get_by_role("button", name="Подключиться").click()
    time.sleep(10)  # ожидание загрузки данных из IPA

    # Поиск устройства
    page.get_by_role("searchbox", name="Поиск:").fill(device_number)
    page.get_by_role("searchbox", name="Поиск:").press("Enter")
    time.sleep(2)

    # Клик по чекбоксу рядом с нужным устройством
    checkbox = page.get_by_role("row", name=f"redos8  {device_number}").get_by_role("checkbox")
    checkbox.click()

    # Импорт устройства
    page.get_by_role("button", name="Импортировать в организацию").click()
    page.get_by_role("insertion").first.click()
    page.get_by_role("button", name="Выполнить").click()
    time.sleep(5)

    # Проверка тоста об успешном импорте
    toast = page.locator("div").filter(has_text=toast_import_success).nth(1)
    toast.wait_for(timeout=timeout)
    toast.click()

    # Переход к разделу устройств
    page.get_by_role("link", name="Устройства").click()
    time.sleep(2)

    # Удаление устройства
    page.get_by_role("gridcell", name=device_number.split()[1]).click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_role("button", name="Удалить").click()
    time.sleep(2)

    # Проверка тоста об удалении
    toast = page.locator("div").filter(has_text=toast_delete_success).nth(1)
    toast.wait_for(timeout=timeout)
    toast.click()
