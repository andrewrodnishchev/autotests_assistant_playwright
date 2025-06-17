import pytest
import time
from playwright.sync_api import expect

def test_create_edit_delete_license(auth_page):
    page = auth_page

    # Переход в раздел "Администрирование → Лицензии"
    page.get_by_role("link", name=" Администрирование ").click()
    time.sleep(1)
    page.get_by_role("link", name=" Лицензии").click()
    time.sleep(1)

    # Создание лицензии
    page.get_by_role("link", name="Создать").click()
    time.sleep(1)
    page.locator("#Comment").fill("тест лицензия")
    time.sleep(0.5)
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div").filter(has_text="Лицензия успешно создана").nth(1)).to_be_visible(timeout=5000)
    time.sleep(1)

    # Поиск по таблице
    page.get_by_role("searchbox", name="Поиск:").fill("тест лицензия")
    page.get_by_role("searchbox", name="Поиск:").press("Enter")
    time.sleep(1)

    # Редактирование
    license_cell = page.get_by_role("gridcell", name="тест лицензия")
    expect(license_cell).to_be_visible(timeout=5000)
    license_cell.click(button="right")
    page.get_by_role("link", name="Изменить").click()
    time.sleep(1)

    # Изменяем статус
    page.locator("#StatusId").select_option("1")  # Активна
    time.sleep(0.5)
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator("div").filter(has_text="Лицензия успешно изменена").nth(1)).to_be_visible(timeout=5000)
    time.sleep(1)

    # Очистка фильтров
    page.locator("#filter-icon").click()
    time.sleep(0.5)
    page.get_by_role("button", name="Активна Активна").click()
    time.sleep(0.5)
    page.locator("li.opt", has_text="Заблокирована").click()
    time.sleep(0.5)
    page.get_by_role("button", name="Применить").click()
    time.sleep(1)

    # Удаление
    license_cell.click(button="right")
    page.get_by_role("link", name="Удалить").click()
    time.sleep(0.5)
    delete_modal = page.get_by_label("Удаление лицензии")
    expect(delete_modal).to_be_visible(timeout=5000)
    delete_modal.get_by_role("button", name="Удалить").click()
    time.sleep(1)

    # Проверка уведомления об удалении
    expect(page.locator("div").filter(has_text="Лицензия успешно удалена").nth(1)).to_be_visible(timeout=5000)
    time.sleep(1)
