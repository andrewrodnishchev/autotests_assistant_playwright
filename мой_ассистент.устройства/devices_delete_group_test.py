from playwright.sync_api import expect
import pytest

def test_add_and_delete_device_group(auth_page):
    page = auth_page

    # Переход в раздел "Мой ассистент" → "Устройства"
    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Устройства").click()

    # Нажимаем "Добавить группу"
    page.get_by_role("link", name="Добавить группу").click()
    page.locator("#Name").click()
    page.locator("#Name").fill("тест 10")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка появления уведомления об успешном создании
    expect(page.locator("div").filter(has_text="Группа устройств успешно создана").nth(1)).to_be_visible(timeout=5000)

    # Удаление созданной группы
    page.get_by_role("gridcell", name="тест 10").locator("span").first.click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_role("button", name="Удалить").click()

    # Проверка уведомления об успешном удалении
    expect(page.locator("div").filter(has_text="Группа устройств успешно удалена").nth(1)).to_be_visible(timeout=5000)
