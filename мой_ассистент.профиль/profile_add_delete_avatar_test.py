import os
import pytest
from playwright.sync_api import Page, expect


def toggle_registration_setting(page: Page):
    page.get_by_role("link", name="Администрирование").click()
    page.get_by_role("link", name="Системные настройки").click()
    page.locator("div:nth-child(3) > .col-sm-10 > .i-checks > .icheckbox_square-green > .iCheck-helper").first.click()
    page.get_by_role("button", name="Сохранить").click()


def test_avatar_upload_and_delete(auth_page: Page):
    page = auth_page

    # Включаем/отключаем чекбокс в начале теста
    toggle_registration_setting(page)

    # Путь к изображению рядом с этим файлом
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "qa.png")

    # Переход в "Мой ассистент" → "Профиль"
    page.get_by_role("link", name="Мой ассистент").click()
    page.get_by_role("link", name="Профиль").click()
    page.get_by_role("link", name="Изменить").click()

    # Загрузка файла
    page.locator('input[type="file"]').set_input_files(image_path)
    page.get_by_role("button", name="Сохранить").click()

    # Проверка сообщения об успешной загрузке
    expect(page.locator(".toast-message", has_text="Аватарка успешно изменена")).to_be_visible(timeout=5000)

    # Удаление аватарки
    page.get_by_role("link", name="Удалить", exact=True).click()
    page.get_by_role("button", name="Удалить").click()

    # Проверка сообщения об успешном удалении
    expect(page.locator(".toast-message", has_text="Аватарка успешно удалена.")).to_be_visible(timeout=5000)

    # Возвращаем чекбокс в начальное состояние
    toggle_registration_setting(page)
