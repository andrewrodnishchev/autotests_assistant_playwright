from playwright.sync_api import Page, expect
import time

def test_add_device_with_cleanup(auth_page: Page):
    page = auth_page
    device_hid = "014917927"
    duplicate_message = "Устройство с таким идентификатором включено"
    success_messages = [
        "Устройство успешно добавлено",
        "Приглашение на включение в организацию успешно добавлено"
    ]
    delete_message = "Успешно удалено устройств: 1 шт"

    # Переходим в тестовую организацию
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()
    time.sleep(1)
    # Попытка добавления устройства
    page.get_by_title("Добавить устройство").click()
    page.locator("#HID").fill(device_hid)
    time.sleep(1)
    # Сохраняем форму с устройством
    page.get_by_role("button", name="Сохранить").click()
    page.get_by_role("button", name="Сохранить").click()

    try:
        # Проверяем наличие сообщения о дубликате
        expect(page.get_by_text(duplicate_message)).to_be_visible(timeout=6000)

        # Если дубликат найден — отменяем и удаляем
        page.get_by_role("link", name="Отмена").click()

        # Ищем устройство в таблице и удаляем
        page.get_by_role("row", name="014 917 927").get_by_role("checkbox").check()
        page.get_by_role("button", name="").click()
        page.get_by_role("button", name="Удалить").click()
        expect(page.get_by_text(delete_message)).to_be_visible(timeout=6000)

        # Повторное добавление
        page.get_by_title("Добавить устройство").click()
        page.locator("#HID").fill(device_hid)
        page.get_by_role("button", name="Сохранить").click()
        page.get_by_role("button", name="Сохранить").click()

    except AssertionError:
        # Дубликата не было — идём дальше
        pass

    # Финальная проверка: любое из двух успешных сообщений
    success_locator = page.locator("div.toast-message").first
    success_text = success_locator.inner_text(timeout=6000)

    assert any(msg in success_text for msg in success_messages), f"Не найдено ожидаемое сообщение. Получено: {success_text}"
