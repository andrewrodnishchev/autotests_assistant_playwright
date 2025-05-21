import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize("device_full, device_short", [("014917927", "917 927")])
def test_add_device_to_collection(auth_page: Page, device_full: str, device_short: str):
    page = auth_page

    # Переход в нужную вкладку
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Коллекции").click()
    page.get_by_text("информация об устройстве").click()

    # Попытка добавить устройство
    page.get_by_title("Добавить устройство").click()
    page.locator("#HID").fill(device_full)
    page.get_by_role("button", name="Сохранить").click()
    page.get_by_role("button", name="Сохранить").click()

    try:
        # Если устройство уже в коллекции
        page.locator("div").filter(has_text="Устройство уже добавлено в коллекцию").nth(1).wait_for(timeout=3000)
        print("⚠️ Устройство уже есть — удаляем и добавляем заново")

        # Отмена добавления
        page.get_by_role("link", name="Отмена").click()

        # Удаление
        page.get_by_role("gridcell", name=device_short).click(button="right")
        page.get_by_role("link", name="Удалить").click()
        page.get_by_role("button", name="Удалить").click()
        page.locator("div").filter(has_text="Устройство успешно удалено").nth(1).wait_for(timeout=3000)

        # Повторное добавление
        page.get_by_title("Добавить устройство").click()
        page.locator("#HID").fill(device_full)
        page.get_by_role("button", name="Сохранить").click()
        page.get_by_role("button", name="Сохранить").click()
        page.locator("div").filter(has_text="Устройство успешно добавлено в коллекцию").nth(1).wait_for(timeout=3000)
        print("✅ Устройство было переустановлено")

    except:
        # Если устройство не было — добавилось сразу
        page.locator("div").filter(has_text="Устройство успешно добавлено в коллекцию").nth(1).wait_for(timeout=3000)
        print("✅ Устройство добавлено без ошибок")
