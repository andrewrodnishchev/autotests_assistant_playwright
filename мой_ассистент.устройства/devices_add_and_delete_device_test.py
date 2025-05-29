from playwright.sync_api import expect
import pytest

def test_add_device_with_duplicate_check(auth_page):
    page = auth_page

    # Переход в раздел "Мой ассистент" → "Устройства"
    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Устройства").click()

    # Добавляем устройство
    page.get_by_role("link", name="Добавить устройство").click()
    page.locator("#HID").fill("014917927")
    page.get_by_role("button", name="Сохранить").click()
    page.get_by_role("button", name="Сохранить").click()

    try:
        # Проверяем, не появилось ли сообщение о дубликате
        expect(page.get_by_text(
            "Устройство с таким идентификатором уже добавлено. Пожалуйста, укажите другое"
        )).to_be_visible(timeout=2000)

        print("⚠ Устройство уже существует. Удаляем и добавляем заново...")

        # Отмена добавления
        page.get_by_role("link", name="Отмена").click()

        # Находим устройство в таблице (пример: по HID, текст "014 917")
        device_cell = page.get_by_role("gridcell", name="014 917 927")
        device_cell.locator("span").first.click(button="right")

        # Удаляем устройство
        page.get_by_role("link", name="Удалить").click()
        page.get_by_role("button", name="Удалить").click()

        # Убедимся, что удалено
        expect(page.locator("div").filter(has_text="Устройство удалено").nth(1)).to_be_visible(timeout=5000)

        # Добавляем снова
        page.get_by_role("link", name="Добавить устройство").click()
        page.locator("#HID").fill("014 917 927")
        page.get_by_role("button", name="Сохранить").click()
        page.get_by_role("button", name="Сохранить").click()

        expect(page.locator("div").filter(has_text="Устройство успешно добавлено").nth(1)).to_be_visible(timeout=5000)
        print("✅ Устройство успешно переустановлено")

    except AssertionError:
        # Ошибки не было — устройство новое
        expect(page.locator("div").filter(has_text="Устройство успешно добавлено").nth(1)).to_be_visible(timeout=5000)
        print("✅ Устройство успешно добавлено")
