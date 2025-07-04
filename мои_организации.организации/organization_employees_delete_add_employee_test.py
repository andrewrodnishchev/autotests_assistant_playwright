import time
from playwright.sync_api import Page, expect

def test_remove_and_add_employee_to_department(auth_page: Page):
    """Удаление сотрудника из отдела и повторное добавление через выпадающий список."""

    page = auth_page
    email = "rodnischev3@mailforspam.com"

    # Переход в раздел "Сотрудники"
    page.get_by_role("link", name="тест андрей").click()
    time.sleep(0.5)
    page.get_by_role("link", name="Сотрудники").click()
    time.sleep(1)

    # Открытие отдела
    page.get_by_text("Новый отдел").click()
    time.sleep(1)

    # Удаление сотрудника из отдела
    page.get_by_role("gridcell", name=email).click(button="right")
    time.sleep(0.3)
    page.get_by_role("link", name="Удалить из отдела").click()
    time.sleep(0.3)
    page.get_by_role("button", name="Удалить").click()
    time.sleep(0.5)

    expect(page.get_by_text("Удалено 1 сотрудников")).to_be_visible(timeout=5000)
    time.sleep(1)

    # Переход к добавлению сотрудника
    page.get_by_title("Добавить сотрудника").click()
    time.sleep(1)

    # Ввод email
    page.locator("#Email").click()
    page.locator("#Email").fill(email)
    time.sleep(0.5)

    # Открываем кастомный выпадающий список отделов (SumoSelect)
    dropdown_toggle = page.locator("div.SumoSelect.sumo_UserGroups")
    dropdown_toggle.click()
    time.sleep(1.5)

    # Кликаем по нужному отделу ("Новый отдел") в списке
    page.locator('div.optWrapper.multiple ul.options li.opt label', has_text="Новый отдел").click()
    time.sleep(1.3)

    # Сохраняем
    page.get_by_role("button", name="Сохранить").click()
    time.sleep(0.5)

    # Проверка на успешность
    expect(page.locator("div", has_text="Изменения успешно выполнены").nth(1)).to_be_visible(timeout=5000)
    time.sleep(1)
