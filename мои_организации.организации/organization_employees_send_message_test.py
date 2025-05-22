import pytest
from playwright.sync_api import Page, expect


def test_send_message_to_employee(auth_page: Page):
    page = auth_page

    # Переход в нужную организацию
    page.get_by_role("link", name="тест андрей").click()

    # Переход в раздел "Сотрудники"
    page.get_by_role("link", name="Сотрудники").click()

    # ПКМ по сотруднику → Отправить сообщение
    page.get_by_role("gridcell", name="rodnischev@safib.ru").click(button="right")
    page.get_by_role("link", name="Отправить сообщение").click()

    # Ввод текста сообщения
    page.locator("#Text").fill("тест смс")

    # Отправка
    page.get_by_role("button", name="Отправить").click()

    # Ожидание подтверждения (уведомление)
    expect(page.locator("div.toast-message", has_text="Сообщение успешно отправлено выбранным сотрудникам (1)")).to_be_visible(timeout=5000)
