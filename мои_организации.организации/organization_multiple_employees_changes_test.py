import pytest
from playwright.sync_api import Page, expect


def test_change_employee_departments(auth_page: Page):
    page = auth_page

    # Переход в раздел "Сотрудники"
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Сотрудники").click()

    # Выбор двух сотрудников
    page.get_by_role("row", name="тест андрей 3 rodnischev3@").get_by_role("checkbox").check()
    page.get_by_role("row", name="андрээ rodnischev12345@").get_by_role("checkbox").check()

    # Нажатие на кнопку редактирования
    page.get_by_role("button", name="").click()

    # Нажатие на выпадающий список "Отделы"
    page.locator("div.sumo_Departments").click()

    # Выбор отделов: "Новый отдел" и "отдел2"
    page.locator("ul.options >> text=Новый отдел").click()
    page.locator("ul.options >> text=отдел2").click()

    # Подтверждение выбора
    page.locator("label:has-text('Администратор')").click()

    # Подтверждение действия
    page.get_by_role("button", name="Выполнить").click()

    # Проверка, что появилось сообщение об успехе
    expect(page.locator("div").filter(has_text="Успешно изменено сотрудников:").nth(1)).to_be_visible()

    # Повторный выбор тех же сотрудников
    page.get_by_role("row", name="тест андрей 3 rodnischev3@").get_by_role("checkbox").check()
    page.get_by_role("row", name="андрээ rodnischev12345@").get_by_role("checkbox").check()

    # Снова нажимаем на редактирование
    page.get_by_role("button", name="").click()
