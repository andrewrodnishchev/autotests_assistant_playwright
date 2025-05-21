import pytest
from playwright.sync_api import expect

def test_access_policy_crud(auth_page):
    page = auth_page

    # Переход к разделу "Политики доступа"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Политики доступа").click()

    # Создание новой политики
    page.get_by_role("link", name="Добавить политику").click()
    page.locator("#Name").fill("тест политика")
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div.toast-message", has_text="Политика доступа успешно создана")).to_be_visible()

    # Редактирование политики
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Description").fill("тест описание")
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div.toast-message", has_text="Политика доступа успешно сохранена")).to_be_visible()

    # Удаление политики
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_label("Удаление политики доступа").get_by_role("button", name="Удалить").click()
    expect(page.locator("div.toast-message", has_text="Политика доступа удалена")).to_be_visible()
