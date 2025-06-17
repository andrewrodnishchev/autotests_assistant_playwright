import pytest
import time
from playwright.sync_api import expect

@pytest.mark.parametrize("title, description, initial_channels, updated_channels", [
    ("тест вид лицензии", "тест описание", "1", "2"),
])
def test_create_edit_delete_license_type(auth_page, title, description, initial_channels, updated_channels):
    page = auth_page

    # Переход в раздел "Администрирование" → "Виды лицензий"
    page.get_by_role("link", name=" Администрирование ").click()
    time.sleep(1)
    page.get_by_role("link", name=" Виды лицензий").click()
    time.sleep(1)

    # Создание новой лицензии
    page.get_by_role("link", name="Создать").click()
    time.sleep(1)
    page.locator("#Title").fill(title)
    time.sleep(0.5)
    page.locator("#ChannelCount").fill(initial_channels)
    time.sleep(0.5)

    # Сохранение
    page.locator('button.btn.btn-primary[type="submit"]').click()
    time.sleep(1.5)

    # Редактирование: находим строку по тексту названия
    row_cell = page.locator("td.s-align-left", has_text=title)
    expect(row_cell).to_be_visible(timeout=5000)
    row_cell.click(button="right")
    time.sleep(0.5)
    page.get_by_role("link", name="Изменить").click()
    time.sleep(1)

    page.locator("#ChannelCount").fill(updated_channels)
    time.sleep(0.5)
    page.locator("#Description").fill(description)
    time.sleep(0.5)

    # Сохранение
    page.locator('button.btn.btn-primary[type="submit"]').click()
    time.sleep(1.5)

    # Удаление: снова находим строку по тексту
    row_cell = page.locator("td.s-align-left", has_text=title)
    expect(row_cell).to_be_visible(timeout=5000)
    row_cell.click(button="right")
    time.sleep(0.5)
    page.get_by_role("link", name="Удалить").click()
    time.sleep(1)

    # Явное ожидание модального окна удаления
    delete_modal = page.get_by_label("Удаление вида лицензии")
    expect(delete_modal).to_be_visible(timeout=5000)
    time.sleep(0.5)

    # Клик по кнопке "Удалить"
    delete_modal.get_by_role("button", name="Удалить").click()
    time.sleep(1.5)

    # Проверка появления уведомления об успешном удалении
    expect(page.locator("div").filter(has_text="Вид лицензии удален").nth(1)).to_be_visible(timeout=5000)
    time.sleep(1)
