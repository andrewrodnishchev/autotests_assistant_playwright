import pytest
import re
from playwright.sync_api import Page, expect


def test_submit_service_request(auth_page: Page):
    """Подача и отказ от обслуживания сервисной организации с предварительной настройкой."""

    page = auth_page
    service_org_id = "1088645596"

    # ---------- Выключение чекбокса "Прямое управление" ----------
    page.get_by_role("link", name=" Администрирование ").click(timeout=5000)
    page.wait_for_timeout(300)
    page.get_by_role("link", name=" Системные настройки").click(timeout=5000)
    page.wait_for_timeout(500)

    checkbox_input = page.locator("input[type='checkbox']").first
    checkbox_helper = page.locator(".iCheck-helper").first
    checkbox_input.wait_for(state="visible", timeout=5000)

    if checkbox_input.is_checked():
        checkbox_helper.click()
        page.wait_for_timeout(300)
        page.get_by_role("button", name="Сохранить").click(timeout=3000)
        page.wait_for_timeout(500)

    # ---------- Основная часть теста ----------
    page.get_by_role("link", name=" Мои организации ").click(timeout=5000)
    page.wait_for_timeout(300)
    page.get_by_role("link", name=" Организации").click(timeout=5000)
    page.wait_for_timeout(300)
    page.get_by_role("link", name="тест андрей").click(timeout=5000)
    page.wait_for_timeout(300)
    page.get_by_role("link", name="Сервисные организации").click(timeout=5000)
    page.wait_for_timeout(300)
    page.get_by_role("link", name="Подать заявку на обслуживание").click(timeout=5000)
    page.wait_for_timeout(300)

    # Подача заявки
    page.get_by_role("textbox").fill(service_org_id, timeout=3000)
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Отправить").click(timeout=3000)
    expect(page.locator("div", has_text="Сервисная организация успешно добавлена").nth(1)).to_be_visible(timeout=7000)
    page.wait_for_timeout(700)

    # Отказ от обслуживания
    page.get_by_role("checkbox").check(timeout=3000)
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Отказаться от обслуживания").click(timeout=3000)
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Отказаться", exact=True).click(timeout=3000)
    page.wait_for_timeout(500)

    # Проверка уведомления об отказе
    toast = page.locator("div.toast-message")
    expect(toast).to_have_text(re.compile("отказ", re.IGNORECASE), timeout=7000)
    page.wait_for_timeout(700)

    # Повторная подача
    page.get_by_role("gridcell", name=service_org_id).click(button="right", timeout=5000)
    page.wait_for_timeout(300)
    page.get_by_text("Подать заявку на обслуживание", exact=True).nth(1).click(timeout=3000)
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Да").click(timeout=3000)
    expect(page.locator("div.toast-message", has_text="Заявка отправлена")).to_be_visible(timeout=7000)
    page.wait_for_timeout(700)

    # Удаление
    page.get_by_role("gridcell", name=service_org_id).click(button="right", timeout=5000)
    page.wait_for_timeout(300)
    page.get_by_role("link", name="Удалить").click(timeout=3000)
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Удалить").click(timeout=3000)
    expect(page.locator("div.toast-message", has_text="Удаление произведено успешно")).to_be_visible(timeout=7000)
    page.wait_for_timeout(700)

    # ---------- Восстановление чекбокса "Прямое управление" ----------
    page.get_by_role("link", name=" Администрирование ").click(timeout=5000)
    page.wait_for_timeout(300)
    page.get_by_role("link", name=" Системные настройки").click(timeout=5000)
    page.wait_for_timeout(500)

    checkbox_input.wait_for(state="visible", timeout=5000)
    if not checkbox_input.is_checked():
        checkbox_helper.click()
        page.wait_for_timeout(300)
        page.get_by_role("button", name="Сохранить").click(timeout=3000)
        expect(page.locator("div.alert.alert-success", has_text="Системные настройки успешно сохранены")).to_be_visible(timeout=5000)
        page.wait_for_timeout(700)
