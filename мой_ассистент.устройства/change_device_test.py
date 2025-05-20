from playwright.sync_api import expect
import pytest

def test_edit_device_description(auth_page):
    page = auth_page

    # Переход в раздел "Мой ассистент" → "Устройства"
    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Устройства").click()

    # Открываем меню устройства " 014 917" и редактируем описание
    page.get_by_role("gridcell", name=" 014 917").locator("span").first.click(button="right")
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Description").click()
    page.locator("#Description").fill("тест коммент")
    page.get_by_role("button", name="Сохранить").click()

    # Проверка появления сообщения об успешном сохранении
    expect(page.locator("div").filter(has_text="Устройство успешно сохранено").nth(1)).to_be_visible(timeout=5000)

    # Снова открываем редактирование и удаляем описание
    page.get_by_role("gridcell", name=" 014 917").locator("span").first.click(button="right")
    page.get_by_role("link", name="Изменить").click()
    page.locator("#Description").click()
    page.locator("#Description").fill("")
    page.get_by_role("button", name="Сохранить").click()

    # Повторная проверка успешного сохранения
    expect(page.locator("div").filter(has_text="Устройство успешно сохранено").nth(1)).to_be_visible(timeout=5000)
