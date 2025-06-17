import time
import pytest
from playwright.sync_api import expect


def test_access_role_crud(auth_page):
    page = auth_page

    # Переход в раздел "Роли доступа"
    page.get_by_role("link", name="Администрирование").click()
    time.sleep(0.5)
    page.get_by_role("link", name="Роли доступа").click()
    time.sleep(0.5)

    # Создание новой роли
    page.get_by_role("link", name="Создать").click()
    time.sleep(0.5)
    page.locator("#Name").fill("тест роль")
    page.get_by_role("button", name="Сохранить").click()

    # Ожидание тоста с текстом об успешном создании
    expect(page.locator("div.toast").filter(has_text="Роль доступа успешно создана")).to_be_visible()

    # Изменение роли: поставить чекбокс
    page.get_by_role("gridcell", name="тест роль").click(button="right")
    time.sleep(0.5)
    page.get_by_role("link", name="Изменить").click()
    page.locator(".iCheck-helper").first.click()
    time.sleep(0.5)
    page.get_by_role("button", name="Сохранить").click()

    # Ожидание тоста с текстом об успешном сохранении
    expect(page.locator("div.toast").filter(has_text="Роль доступа успешно сохранена")).to_be_visible()

    # Удаление роли
    page.get_by_role("gridcell", name="тест роль").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_label("Удаление роли доступа").get_by_role("button", name="Удалить").click()

    # Ожидание тоста с текстом об удалении
    expect(page.locator("div.toast").filter(has_text="Роль доступа удалена")).to_be_visible()
