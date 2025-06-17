import pytest
from playwright.sync_api import Page, expect


def test_request_category_crud(auth_page: Page):
    page = auth_page

    # Переход в раздел "Категории заявок"
    page.get_by_role("link", name=" Администрирование ").click()
    page.get_by_role("link", name=" Категории заявок").click()

    # Создание категории
    page.get_by_role("link", name="Создать").click()
    page.locator("#Name").fill("тест заявки")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка тоста после создания
    expect(page.locator("div.toast").filter(has_text="Категория заявок создана")).to_be_visible()

    # Редактирование категории
    page.get_by_role("gridcell", name="тест заявки").click(button="right")
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Name").fill("тест заявки 2")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка тоста после сохранения
    expect(page.locator("div.toast").filter(has_text="Категория заявок успешна сохранена")).to_be_visible()

    # Удаление категории
    page.get_by_role("gridcell", name="тест заявки").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_label("Удаление категории заявок").get_by_role("button", name="Удалить").click()

    # Проверка тоста после удаления
    expect(page.locator("div.toast").filter(has_text="Категория заявок удалена")).to_be_visible()
