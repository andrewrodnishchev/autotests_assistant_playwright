import pytest
from playwright.sync_api import expect, Page


def test_department_crud(auth_page: Page):
    page = auth_page

    # Переход в раздел "Сотрудники"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Сотрудники").click()

    # Добавление отдела
    page.get_by_title("Добавить отдел").click()
    page.locator("#Name").fill("тест отдел")
    page.get_by_role("button", name="Сохранить").click()

    # Редактирование отдела
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Description").fill("тест описание")
    page.get_by_role("button", name="Сохранить").click()

    # Назад к списку
    page.get_by_role("link", name="Назад").click()

    # Удаление отдела
    page.get_by_role("gridcell", name="тест отдел").click(button="right")
    page.get_by_role("link", name="Удалить").click()
    page.get_by_role("button", name="Удалить").click()

    # Проверка, что отдел исчез из списка
    expect(page.get_by_role("gridcell", name="тест отдел")).not_to_be_visible(timeout=5000)
