import pytest
import re
from datetime import datetime, timedelta
from playwright.sync_api import Page, expect


def parse_email_time(date_str):
    date_str = date_str.lower()
    now = datetime.now()
    try:
        if "сегодня" in date_str:
            time_part = date_str.split(",")[1].strip()
            dt = datetime.strptime(time_part, "%H:%M")
            return now.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)
        elif "вчера" in date_str:
            time_part = date_str.split(",")[1].strip()
            dt = datetime.strptime(time_part, "%H:%M")
            yesterday = now.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0) - timedelta(days=1)
            return yesterday
        else:
            dt = datetime.strptime(date_str, "%d.%m.%Y, %H:%M")
            return dt
    except Exception:
        return None


@pytest.mark.usefixtures("page", "context")
def test_change_email_and_confirm(page: Page, context):
    # --- Вход под админом и переключение системной настройки ---
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")
    page.get_by_role("textbox", name="Email или Логин").click()
    page.get_by_role("textbox", name="Email или Логин").fill("rodnischev@safib.ru")
    page.get_by_role("textbox", name="Пароль").click()
    page.get_by_role("textbox", name="Пароль").fill("1")
    page.get_by_role("button", name="Вход").click()
    page.get_by_role("link", name="Администрирование").click()
    page.get_by_role("link", name="Системные настройки").click()
    page.locator("div:nth-child(3) > .col-sm-10 > .i-checks > .icheckbox_square-green > .iCheck-helper").first.click()
    page.get_by_role("button", name="Сохранить").click()
    page.get_by_role("link", name="Андрей Роднищев").click()
    page.get_by_role("link", name="Выход").click()

    # --- Основной тест смены почты и подтверждения ---
    base_email = "ast123@mailforspam.com"
    new_email = "ast1233@mailforspam.com"

    # Вход под базовым пользователем
    page.get_by_role("textbox", name="Email или Логин").click()
    page.get_by_role("textbox", name="Email или Логин").fill(base_email)
    page.get_by_role("textbox", name="Пароль").click()
    page.get_by_role("textbox", name="Пароль").fill("1")
    page.get_by_role("button", name="Вход").click()

    # Переход в профиль, смена почты
    page.get_by_role("link", name="Мой ассистент").click()
    page.get_by_role("link", name="Профиль").click()
    page.get_by_role("link", name=base_email).nth(0).click()
    page.locator("#Email").fill(new_email)
    page.get_by_role("button", name="Сохранить").click()
    expect(page.get_by_text("Введите код подтверждения")).to_be_visible(timeout=10000)

    # Проверяем почту для подтверждения новой почты
    mail_page = context.new_page()
    mail_page.goto(f"https://www.mailforspam.com/mail/{new_email.split('@')[0]}",
                   wait_until="domcontentloaded", timeout=15000)
    mail_page.wait_for_timeout(3000)
    mail_page.reload(wait_until="domcontentloaded")
    mail_page.get_by_role("button", name="Check").click()
    mail_page.wait_for_selector('a:has-text("Подтверждение адреса электронной почты")', timeout=15000)

    emails = mail_page.locator('a:has-text("Подтверждение адреса электронной почты")')
    email_count = emails.count()
    assert email_count > 0, "Письма не найдены"

    latest_email_index = 0
    latest_email_time = None

    for i in range(email_count):
        date_text = mail_page.locator(f'xpath=(//a[contains(text(),"Подтверждение адреса электронной почты")])[{i+1}]/ancestor::tr/td[last()]').text_content()
        dt = parse_email_time(date_text)
        if dt and (latest_email_time is None or dt > latest_email_time):
            latest_email_time = dt
            latest_email_index = i

    emails.nth(latest_email_index).click()
    mail_page.wait_for_selector('text=код подтверждения', timeout=10000)
    email_text = mail_page.content()
    match = re.search(r"код подтверждения (\d{3})", email_text)
    assert match, "Код подтверждения не найден в письме"
    code = match.group(1)

    # Вводим код подтверждения
    page.bring_to_front()
    page.get_by_role("textbox", name="Введите код подтверждения").fill(code)
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator(".toast-message", has_text="Адрес электронной почты изменен")).to_be_visible(timeout=5000)

    # Логинимся под новой почтой
    page.get_by_role("textbox", name="Email или Логин").fill(new_email)
    page.get_by_role("textbox", name="Пароль").fill("1")
    page.get_by_role("button", name="Вход").click()

    # Переход в профиль, смена обратно на старую почту
    page.get_by_role("link", name=new_email).click()
    page.locator("#Email").click()
    page.locator("#Email").fill(base_email)
    page.get_by_role("button", name="Сохранить").click()
    expect(page.get_by_text("Введите код подтверждения")).to_be_visible(timeout=10000)

    # Проверяем почту для подтверждения обратной смены
    mail_page2 = context.new_page()
    mail_page2.goto(f"https://www.mailforspam.com/mail/{base_email.split('@')[0]}",
                    wait_until="domcontentloaded", timeout=15000)
    mail_page2.wait_for_timeout(3000)
    mail_page2.reload(wait_until="domcontentloaded")
    mail_page2.get_by_role("button", name="Check").click()
    mail_page2.wait_for_selector('a:has-text("Подтверждение адреса электронной почты")', timeout=15000)

    emails2 = mail_page2.locator('a:has-text("Подтверждение адреса электронной почты")')
    email_count2 = emails2.count()
    assert email_count2 > 0, "Письма не найдены"

    latest_email_index2 = 0
    latest_email_time2 = None

    for i in range(email_count2):
        date_text = mail_page2.locator(f'xpath=(//a[contains(text(),"Подтверждение адреса электронной почты")])[{i+1}]/ancestor::tr/td[last()]').text_content()
        dt = parse_email_time(date_text)
        if dt and (latest_email_time2 is None or dt > latest_email_time2):
            latest_email_time2 = dt
            latest_email_index2 = i

    emails2.nth(latest_email_index2).click()
    mail_page2.wait_for_selector('text=код подтверждения', timeout=10000)
    email_text2 = mail_page2.content()
    match2 = re.search(r"код подтверждения (\d{3})", email_text2)
    assert match2, "Код подтверждения не найден в письме"
    code2 = match2.group(1)

    # Вводим код подтверждения обратной смены
    page.bring_to_front()
    page.get_by_role("textbox", name="Введите код подтверждения").fill(code2)
    page.get_by_role("button", name="Сохранить").click()
    expect(page.locator(".toast-message", has_text="Адрес электронной почты изменен")).to_be_visible(timeout=5000)

    # --- В конце выход и повторный логин админом с переключением чекбокса ---
    # Ждем появления элемента, затем кликаем по ссылке пользователя, иначе fallback — просто логин
    try:
        user_link = page.get_by_role("listitem").filter(has_text=f"{base_email} ast123")
        user_link.get_by_role("link").wait_for(state="visible", timeout=10000)
        user_link.get_by_role("link").click()
    except Exception:
        # Если элемент не найден, пропускаем к логину админа
        print("Пользовательская ссылка не найдена, пропускаем к логину админа")


    page.get_by_role("textbox", name="Email или Логин").click()
    page.get_by_role("textbox", name="Email или Логин").fill("rodnischev@safib.ru")
    page.get_by_role("textbox", name="Пароль").click()
    page.get_by_role("textbox", name="Пароль").fill("1")
    page.get_by_role("button", name="Вход").click()
    page.get_by_role("link", name="Администрирование").click()
    page.get_by_role("link", name="Системные настройки").click()
    page.locator("div:nth-child(3) > .col-sm-10 > .i-checks > .icheckbox_square-green > .iCheck-helper").first.click()
    page.get_by_role("button", name="Сохранить").click()
