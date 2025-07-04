import re
import time
import pytest
from playwright.sync_api import Page, Browser, expect

ENVIRONMENTS = {
    'corp': {
        'base_url': 'http://lk.corp.dev.ru',
        'login': 'rodnischev3@mailforspam.com',
        'password': '1',
        'timeout': 45000
    },
    'setup': {
        'base_url': 'http://office.setuplk.ru',
        'login': 'rodnischev3@mailforspam.com',
        'password': '1',
        'timeout': 45000
    }
}

def get_code_from_mail(mail_page: Page, login: str) -> str:
    mail_page.goto(f"https://www.mailforspam.com/mail/{login}", wait_until="commit", timeout=5000)
    time.sleep(3)
    mail_page.locator("#input_box").press("Enter")

    latest_mail_row = mail_page.locator("tr[onclick]").first
    latest_mail_row.click()

    bold_code = mail_page.locator("b").first.inner_text().strip()

    if not re.fullmatch(r"\d{6,7}", bold_code):
        raise ValueError(f"Полученное значение не похоже на код: {bold_code}")

    return bold_code

@pytest.mark.parametrize("browser", ["chromium"], indirect=True)
def test_full_2fa_flow(browser: Browser, request):
    # Получаем имя окружения из параметра pytest --env, если не указано — 'corp'
    env_name = request.config.getoption("--env") if hasattr(request.config, "getoption") else "corp"
    env = ENVIRONMENTS.get(env_name, ENVIRONMENTS["corp"])

    base_url = env['base_url']
    login = env['login']
    password = env['password']

    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    # ========== ЧАСТЬ 1: Включаем двухфакторку ==========
    page.goto(f"{base_url}/Account/Login?returnUrl=%2FClientOrg")
    page.get_by_role("textbox", name="Email или Логин").fill(login)
    page.get_by_role("textbox", name="Пароль").fill(password)
    page.get_by_role("button", name="Вход").click()

    page.get_by_role("link", name="тест андрей").click()
    page.locator("a.btn.btn-primary.profile").click()
    page.get_by_role("link", name="Безопасность").click()

    page.get_by_role("insertion").click()
    time.sleep(1)
    toast = page.locator("div.toast-message", has_text="Тип аутентификации успешно изменен")
    expect(toast).to_be_visible()
    toast.click()

    # ========== ЧАСТЬ 2: Перелогиниваемся с 2FA ==========
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Выход").click()

    page.get_by_role("textbox", name="Email или Логин").fill(login)
    page.get_by_role("textbox", name="Пароль").fill(password)
    page.get_by_role("button", name="Вход").click()

    mail_page = context.new_page()
    code = get_code_from_mail(mail_page, login.split('@')[0])

    time.sleep(5)
    mail_page.close()

    page.get_by_role("textbox", name="Код подтверждения").fill(code)
    page.get_by_role("button", name="Вход в личный кабинет").click()

    expect(page.get_by_role("link", name="тест андрей")).to_be_visible()

    page.get_by_role("link", name="тест андрей").click()
    page.locator("a.btn.btn-primary.profile").click()
    page.get_by_role("link", name="Безопасность").click()
    page.get_by_role("insertion").first.click()
    expect(page.locator("div.toast-message", has_text="Тип аутентификации успешно изменен")).to_be_visible()

    context.close()
