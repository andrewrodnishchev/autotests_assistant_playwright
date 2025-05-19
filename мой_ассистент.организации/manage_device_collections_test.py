import pytest
from playwright.sync_api import Page, expect


def test_manage_device_collections(auth_page: Page):
    """Добавление и удаление устройства в/из коллекции, проверка успешных операций."""
    page = auth_page

    # Переход в раздел "Коллекции"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Коллекции").click()

    # Удаление устройства из коллекции (если оно уже там)
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_role("button", name="Удалить").click()
    expect(page.locator("div").filter(has_text="Устройства успешно удалены").nth(1))

    # Добавление устройства в коллекцию
    page.get_by_role("link", name="Устройства").click()
    page.get_by_role("row", name="014 917 927 c405-Andrey2").get_by_role("checkbox").check()
    page.get_by_role("button", name="").click()  # "Добавить в коллекцию"
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div").filter(has_text="Устройств добавлено в коллекцию:").nth(1)).to_be_visible(timeout=5000)

    # Проверка обновления коллекции и повторное удаление
    page.get_by_role("link", name="Коллекции").click()
    page.locator("#DeviceCollectionTableNew_90_refresh").click()
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_role("button", name="Удалить").click()
    expect(page.locator("div").filter(has_text="Устройство успешно удалено").nth(1)).to_be_visible(timeout=5000)

    # Повторное добавление устройства в коллекцию через контекстное меню
    page.get_by_role("link", name="Устройства").click()
    page.get_by_role("gridcell", name="917 927").click(button="right")
    page.get_by_role("link", name="Добавить в коллекцию").click()
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div").filter(has_text="Устройств добавлено в коллекцию:").nth(1)).to_be_visible(timeout=5000)
