import pytest
from playwright.sync_api import expect

def test_access_policy_security_settings(auth_page):
    page = auth_page

    # Переход в раздел "Политики доступа"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Политики доступа").click()

    # Создание новой политики
    page.get_by_role("link", name="Добавить политику").click()
    page.locator("#Name").fill("тест политика")
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div", has_text="Политика доступа успешно создана").nth(1)).to_be_visible()

    # Открытие редактирования
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Изменить").click()

    # Переход во вкладку "Безопасность"
    page.get_by_role("link", name="Безопасность").click()

    # Настройка параметров безопасности
    page.locator("#DynamicPasswordTypeId").select_option("3")  # Выбор типа пароля

    # Сохранение изменений
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div", has_text="Политика доступа успешно сохранена").nth(1)).to_be_visible()

    # Удаление политики
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_label("Удаление политики доступа").get_by_role("button", name="Удалить").click()
    expect(page.locator("div", has_text="Политика доступа удалена").nth(1)).to_be_visible()
