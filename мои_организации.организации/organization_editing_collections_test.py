import pytest
from playwright.sync_api import Page, expect


def test_create_edit_delete_collection(auth_page: Page):
    page = auth_page

    # Переход к разделу "Коллекции"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Коллекции").click()

    # Добавление новой коллекции
    page.get_by_title("Добавить коллекцию").click()
    page.locator("#Name").fill("тест коллекция")
    page.get_by_role("button", name="Сохранить").click()
    expect(
        page.locator("div").filter(has_text="Коллекция успешно добавлена").nth(1)
    ).to_be_visible()

    # Редактирование коллекции
    page.get_by_text("тест коллекция").click(button="right")
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Name").fill("тест коллекция 2")
    page.locator("#Description").fill("123")
    page.get_by_role("button", name="Сохранить").click()
    expect(
        page.locator("div").filter(has_text="Коллекция успешно изменена").nth(1)
    ).to_be_visible()

    # Удаление коллекции
    page.get_by_text("тест коллекция").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_role("button", name="Удалить").click()
