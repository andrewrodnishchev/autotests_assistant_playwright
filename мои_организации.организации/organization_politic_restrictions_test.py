import pytest
from playwright.sync_api import expect, Page


def test_access_policy_crud(auth_page: Page):
    page = auth_page

    # Переход в клиентскую организацию
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Политики доступа").click()

    # Создание политики доступа
    page.get_by_role("link", name="Добавить политику").click()
    page.locator("#Name").click()
    page.locator("#Name").fill("тест политика")
    page.get_by_role("button", name="Сохранить").click()

    expect(page.locator("div").filter(has_text="Политика доступа успешно создана").nth(1)).to_be_visible()

    # Редактирование политики
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Изменить").click()
    page.get_by_role("link", name="Ограничения").click()

    # Включаем чекбоксы и радиокнопки
    page.locator("#tab-3 > .panel-body > div:nth-child(3) .iCheck-helper").click()
    page.locator("#tab-3 > .panel-body > div:nth-child(4) .iCheck-helper").click()
    page.locator("#tab-3 > .panel-body > div:nth-child(6) .iCheck-helper").click()
    page.locator("#tab-3 > .panel-body > div:nth-child(5) .iCheck-helper").click()

    page.locator("#tab-3 > .panel-body > div:nth-child(10) > .col-sm-10 > div:nth-child(2) .iCheck-helper").click()
    page.locator("#tab-3 > .panel-body > div:nth-child(10) > .col-sm-10 > div:nth-child(3) .iCheck-helper").click()
    page.locator("#tab-3 > .panel-body > div:nth-child(10) > .col-sm-10 > div:nth-child(4) .iCheck-helper").click()

    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div").filter(has_text="Политика доступа успешно сохранена").nth(1)).to_be_visible()

    # Удаление политики
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_label("Удаление политики доступа").get_by_role("button", name="Удалить").click()
    expect(page.locator("div").filter(has_text="Политика доступа удалена").nth(1)).to_be_visible()
