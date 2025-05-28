from playwright.sync_api import Page, expect

def test_add_device_with_cleanup(auth_page: Page):
    page = auth_page
    device_hid = "014917927"
    duplicate_message = "Устройство с таким идентификатором включено"
    success_message = "Устройство успешно добавлено"
    delete_message = "Успешно удалено устройств: 1 шт"

    # Переходим в тестовую организацию
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Попытка добавления устройства
    page.get_by_title("Добавить устройство").click()
    page.locator("#HID").fill(device_hid)

    # Сохраняем форму с устройством
    page.get_by_role("button", name="Сохранить").click()
    page.get_by_role("button", name="Сохранить").click()

    try:
        # Проверяем наличие сообщения о дубликате (ждем 3 секунды)
        expect(page.get_by_text(duplicate_message)).to_be_visible(timeout=6000)

        # Если дубликат найден - отменяем и удаляем
        page.get_by_role("link", name="Отмена").click()

        # Ищем устройство в таблице
        page.get_by_role("row", name="014 917 927").get_by_role("checkbox").check()

        # Удаляем устройство
        page.get_by_role("button", name="").click()
        page.get_by_role("button", name="Удалить").click()
        expect(page.get_by_text(delete_message)).to_be_visible(timeout=6000)

        # Повторно добавляем устройство
        page.get_by_title("Добавить устройство").click()
        page.locator("#HID").fill(device_hid)
        page.get_by_role("button", name="Сохранить").click()
        page.get_by_role("button", name="Сохранить").click()

    except AssertionError:
        # Если дубликат не найден - просто проверяем успешное добавление
        pass

    # Финальная проверка успешного добавления
    expect(page.get_by_text(success_message)).to_be_visible(timeout=6000)
