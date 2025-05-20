import pytest
import re
from playwright.sync_api import Page, expect


def test_add_and_delete_device_group(auth_page: Page):
    """Добавление новой группы устройств и её удаление."""
    page = auth_page

    # Переход в раздел Устройства
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Добавление новой группы
    page.get_by_title("Добавить группу").click()
    page.locator("#Name").fill("тест2")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка сообщения об успешном создании
    success_message = page.locator("div").filter(has_text="Группа устройств успешно создана").nth(1)
    expect(success_message).to_be_visible(timeout=5000)

    # Возврат назад
    page.get_by_role("link", name="Назад").click()

    # Поиск добавленной группы и клик по иконке меню
    pattern = re.compile(r"тест2.*")
    row = page.get_by_role("row", name=pattern)
    expect(row).to_be_visible(timeout=5000)
    row.locator("i").click()

    # Клик по удалению группы и подтверждение
    page.get_by_role("link", name="Удалить").click()
    page.get_by_role("button", name="Удалить").click()

    # (Опционально) Проверка, что группа больше не отображается
    expect(page.get_by_role("row", name=pattern)).not_to_be_visible(timeout=5000)

