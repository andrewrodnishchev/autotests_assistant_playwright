import pytest
import time
from playwright.sync_api import Page, expect


def test_manage_device_collections(auth_page: Page):
    """Добавление и удаление устройства в/из коллекции, проверка успешных операций."""
    page = auth_page

    # Переход в раздел "Коллекции"
    page.get_by_role("link", name="тест андрей").click()
    time.sleep(1)
    page.get_by_role("link", name="Коллекции").click()
    time.sleep(1)

    # Удаление устройства из коллекции (если оно уже там)
    page.get_by_role("gridcell", name="917 927").click(button="right")
    time.sleep(0.5)
    page.get_by_role("link", name="Удалить").click()
    time.sleep(0.5)
    page.get_by_role("button", name="Удалить").click()
    expect(page.locator("div.toast-message", has_text="Устройство успешно удалено")).to_be_visible(timeout=5000)
    time.sleep(1)

    # Добавление устройства в коллекцию
    page.get_by_role("link", name="Устройства").click()
    time.sleep(1)
    page.get_by_role("row", name="014 917 927").get_by_role("checkbox").check()
    time.sleep(0.5)
    page.get_by_role("button", name="").click()  # "Добавить в коллекцию"
    time.sleep(0.5)
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div").filter(has_text="Устройств добавлено в коллекцию:").nth(1)).to_be_visible(timeout=5000)
    time.sleep(1)

    # Проверка обновления коллекции и повторное удаление
    page.get_by_role("link", name="Коллекции").click()
    time.sleep(1)
    page.locator("#DeviceCollectionTableNew_90_refresh").click()
    time.sleep(1)
    page.get_by_role("gridcell", name="917 927").click(button="right")
    time.sleep(0.5)
    page.get_by_role("link", name="Удалить").click()
    time.sleep(0.5)
    page.get_by_role("button", name="Удалить").click()
    expect(page.locator("div.toast-message", has_text="Устройство успешно удалено")).to_be_visible(timeout=5000)
    time.sleep(1)

    # Повторное добавление устройства в коллекцию через контекстное меню
    page.get_by_role("link", name="Устройства").click()
    time.sleep(1)
    page.get_by_role("gridcell", name="917 927").click(button="right")
    time.sleep(0.5)
    page.get_by_role("link", name="Добавить в коллекцию").click()
    time.sleep(0.5)
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div").filter(has_text="Устройств добавлено в коллекцию:").nth(1)).to_be_visible(timeout=5000)