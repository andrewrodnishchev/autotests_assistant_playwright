from playwright.sync_api import expect
import pytest

def test_edit_device_group_name(auth_page):
    page = auth_page

    # Переход в "Мой ассистент" → "Устройства"
    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Устройства").click()

    # Правый клик по строке с именем "тест 1"
    page.get_by_role("gridcell", name="тест 1").locator("span").first.click(button="right")
    page.get_by_role("link", name="Изменить").click()

    # Изменяем имя на "тест 1.1"
    page.locator("#Name").click()
    page.locator("#Name").fill("тест 1.1")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка на успех
    expect(page.locator("div").filter(has_text="Группа устройств успешно изменена").nth(1)).to_be_visible(timeout=5000)

    # Снова находим уже переименованную группу и возвращаем название обратно
    page.get_by_role("gridcell", name="тест 1.1").locator("span").first.click(button="right")
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Name").click()
    page.locator("#Name").fill("тест 1")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка на успех
    expect(page.locator("div").filter(has_text="Группа устройств успешно изменена").nth(1)).to_be_visible(timeout=5000)
