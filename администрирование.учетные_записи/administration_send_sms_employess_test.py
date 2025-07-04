import time
import pytest
from playwright.sync_api import Page, expect
from conftest import get_current_environment, ENVIRONMENTS

def test_send_message_to_account(auth_page: Page, request):
    env = get_current_environment(request)
    config = ENVIRONMENTS[env]
    page = auth_page

    # Переход в "Администрирование" → "Учетные записи"
    page.get_by_role("link", name=" Администрирование ").click()
    time.sleep(1)
    page.get_by_role("link", name=" Учетные записи").click()
    time.sleep(1)

    # Поиск учетной записи
    page.get_by_role("searchbox", name="Поиск:").click()
    page.get_by_role("searchbox", name="Поиск:").fill(config["login"])
    page.get_by_role("searchbox", name="Поиск:").press("Enter")
    time.sleep(2)

    # Контекстное меню по ячейке с email → Отправить сообщение
    page.get_by_role("gridcell", name=config["login"]).click(button="right")
    page.get_by_role("link", name="Отправить сообщение").click()
    time.sleep(1)

    # Ввод текста и отправка
    page.locator("#Text").fill("тест")
    page.get_by_role("button", name="Отправить", exact=True).click()
    time.sleep(1)

    # Проверка сообщения об успешной отправке
    expect(page.locator("div").filter(has_text="Сообщение успешно отправлено").nth(1)).to_be_visible(timeout=5000)
