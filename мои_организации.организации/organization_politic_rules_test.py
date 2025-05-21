import pytest
from playwright.sync_api import expect

def test_access_policy_with_rules(auth_page):
    page = auth_page

    # Переход к разделу "Политики доступа"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Политики доступа").click()

    # Создание новой политики
    page.get_by_role("link", name="Добавить политику").click()
    page.locator("#Name").fill("тест политика")
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div", has_text="Политика доступа успешно создана").nth(1)).to_be_visible()

    # Редактирование политики — открытие Правил доступа
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Изменить").click()
    page.get_by_role("link", name="Правила доступа").click()

    # Установка чекбоксов (доступа)
    page.locator(".iCheck-helper").first.click()
    page.locator("div:nth-child(3) > .iradio_square-green > .iCheck-helper").first.click()
    page.get_by_role("insertion").nth(1).click()
    page.locator(".iCheck-helper").first.click()
    page.locator("div:nth-child(2) > .iradio_square-green > .iCheck-helper").first.click()
    page.locator("div:nth-child(3) > .iradio_square-green > .iCheck-helper").first.click()

    # Сохранение политики
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div", has_text="Политика доступа успешно сохранена").nth(1)).to_be_visible()

    # Удаление политики
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_label("Удаление политики доступа").get_by_role("button", name="Удалить").click()
    expect(page.locator("div", has_text="Политика доступа удалена").nth(1)).to_be_visible()
