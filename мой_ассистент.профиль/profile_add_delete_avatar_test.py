import os
import pytest
from playwright.sync_api import Page, expect


def test_avatar_upload_and_delete(auth_page: Page):
    # Путь к изображению рядом с этим файлом
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "qa.png")

    # Переход в "Мой ассистент" → "Профиль"
    auth_page.get_by_role("link", name=" Мой ассистент ").click()
    auth_page.get_by_role("link", name=" Профиль").click()
    auth_page.get_by_role("link", name="Изменить").click()

    # Загрузка файла (возможно, понадобится уточнение input'а)
    auth_page.locator('input[type="file"]').set_input_files(image_path)
    auth_page.get_by_role("button", name="Сохранить").click()

    # Проверка сообщения об успешной загрузке
    expect(auth_page.locator(".toast-message", has_text="Аватарка успешно изменена")).to_be_visible(timeout=5000)


    # Удаление аватарки
    auth_page.get_by_role("link", name="Удалить", exact=True).click()
    auth_page.get_by_role("button", name="Удалить").click()

    # Проверка сообщения об успешном удалении
    expect(auth_page.locator(".toast-message", has_text="Аватарка успешно удалена.")).to_be_visible(timeout=5000)

