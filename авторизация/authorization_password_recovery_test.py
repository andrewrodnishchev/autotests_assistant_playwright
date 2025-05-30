import pytest
from playwright.sync_api import Page, expect

def test_password_recovery(page: Page):
    # Шаг 1. Перейти на страницу восстановления пароля
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")
    page.wait_for_timeout(500)  # небольшая пауза после загрузки страницы

    page.get_by_title("Восстановление пароля").click()
    page.wait_for_timeout(500)  # пауза после перехода на форму восстановления

    page.get_by_role("textbox", name="Электронная почта").fill("ast123@mailforspam.com")
    page.wait_for_timeout(300)  # пауза перед нажатием кнопки

    page.get_by_role("button", name="Восстановить доступ").click()
    page.wait_for_timeout(500)  # пауза перед проверкой подтверждения

    # Подтверждение, что письмо отправлено
    expect(page.get_by_text("письмо")).to_be_visible(timeout=5000)

    # Шаг 2. Открыть почту
    context = page.context
    mail_page = context.new_page()
    mail_page.goto("https://www.mailforspam.com/mail/ast123", wait_until="domcontentloaded", timeout=15000)
    mail_page.wait_for_timeout(1000)  # подождать загрузку инициализации скриптов на странице

    mail_page.get_by_role("button", name="Check").click()
    mail_page.wait_for_timeout(2000)  # подождать обновление писем

    # Ожидание письма
    recovery_link = mail_page.get_by_role("link", name="Восстановление доступа").first
    expect(recovery_link).to_be_visible(timeout=15000)
    recovery_link.click()
    mail_page.wait_for_timeout(1000)  # пауза после открытия письма

    # Переход по ссылке в письме
    mail_page.get_by_role("link", name="ссылке").click()
    mail_page.wait_for_timeout(1000)  # дать странице восстановленного пароля прогрузиться

    # Ввод нового пароля
    mail_page.get_by_role("textbox", name="Пароль", exact=True).fill("1")
    mail_page.wait_for_timeout(300)
    mail_page.get_by_role("textbox", name="Подтвердите пароль").fill("1")
    mail_page.wait_for_timeout(300)

    mail_page.get_by_role("button", name="Создать и войти").click()

    # Проверка перехода на нужную страницу
    mail_page.wait_for_url("**/ClientDevice", timeout=10000)
    assert "/ClientDevice" in mail_page.url, f"Ожидался переход на ClientDevice, но текущий URL: {mail_page.url}"
