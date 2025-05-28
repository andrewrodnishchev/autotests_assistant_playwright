import pytest
from playwright.sync_api import Page, expect


def test_create_edit_delete_inventory_policy(auth_page: Page):
    page = auth_page

    # Переход в раздел политик
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Политики инвентаризации").click()
    page.get_by_role("link", name="Добавить политику").click()

    # Ввод имени политики
    page.locator("#Name").click()
    page.locator("#Name").fill("тест политика")

    # Клик по кнопке "Сохранить"
    save_button = page.locator("button.btn.btn-primary[type='submit']")
    expect(save_button).to_be_visible()
    save_button.click()

    # Ожидание уведомления о создании
    notification = page.locator("div").filter(has_text="Политика инвентаризации успешно добавлена в организацию").nth(1)
    expect(notification).to_be_visible(timeout=5000)
    notification.click()

    # Правый клик по созданной политике и переход к редактированию
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Изменить").click()

    # Изменение: клик по чекбоксу
    page.locator(".iCheck-helper").first.click()

    # Клик по кнопке "Сохранить"
    save_button = page.locator("button.btn.btn-primary[type='submit']")
    expect(save_button).to_be_visible()
    save_button.click()

    # Уведомление об успешном сохранении
    saved_notification = page.locator("div").filter(has_text="Политика инвентаризации успешно сохранена").nth(1)
    expect(saved_notification).to_be_visible(timeout=5000)
    saved_notification.click()

    # Правый клик по политике снова и удаление
    page.get_by_role("gridcell", name="тест политика").click(button="right")
    page.get_by_role("link", name="Удалить").click()

    # Подтверждение удаления
    page.get_by_label("Удаление политики инвентаризации").get_by_role("button", name="Удалить").click()

    # Уведомление об удалении
    deleted_notification = page.locator("div").filter(has_text="Политика инвентаризации удалена").nth(1)
    expect(deleted_notification).to_be_visible(timeout=5000)
    deleted_notification.click()
