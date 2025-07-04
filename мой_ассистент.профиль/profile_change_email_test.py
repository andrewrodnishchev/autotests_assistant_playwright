import re
import pytest
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

def get_checkbox_state(page: Page) -> bool:
    """Проверяет состояние чекбокса самостоятельной регистрации"""
    checkbox = page.locator("input#IsSelfRegistrationAveeble")
    return checkbox.evaluate("el => el.checked")

def toggle_checkbox_safe(page: Page, enable: bool):
    """Безопасное переключение чекбокса с проверкой состояния"""
    current_state = get_checkbox_state(page)

    if enable != current_state:
        # Кликаем на вспомогательный элемент, как в оригинальном тесте
        page.locator("div:nth-child(3) > .col-sm-10 > .i-checks > .icheckbox_square-green > .iCheck-helper").first.click()
        page.wait_for_timeout(500)

        # Проверяем, что состояние изменилось
        new_state = get_checkbox_state(page)
        assert new_state == enable, f"Состояние чекбокса не изменилось. Ожидалось: {enable}, текущее: {new_state}"

def get_confirmation_code(page: Page, email_prefix: str) -> str:
    """Получает код подтверждения из почты в новой вкладке"""
    # Открываем новую вкладку для почты
    with page.context.new_page() as mail_page:
        mail_page.goto(f"https://www.mailforspam.com/mail/{email_prefix}",
                       wait_until="domcontentloaded", timeout=15000)
        mail_page.wait_for_timeout(3000)
        mail_page.reload(wait_until="domcontentloaded")
        mail_page.get_by_role("button", name="Check").click()

        mail_page.wait_for_selector('a:has-text("Подтверждение адреса электронной почты")', timeout=15000)
        emails = mail_page.locator('a:has-text("Подтверждение адреса электронной почты")')
        assert emails.count() > 0, "Письма не найдены"

        # Находим самое свежее письмо
        latest_index, latest_time = 0, None
        for i in range(emails.count()):
            date_text = mail_page.locator(
                f'xpath=(//a[contains(text(),"Подтверждение адреса электронной почты")])[{i+1}]/ancestor::tr/td[last()]').text_content()
            dt = parse_email_time(date_text)
            if dt and (not latest_time or dt > latest_time):
                latest_time, latest_index = dt, i

        emails.nth(latest_index).click()
        mail_page.wait_for_selector('text=код подтверждения', timeout=10000)
        email_text = mail_page.content()
        match = re.search(r"код подтверждения (\d{3})", email_text)
        assert match, "Код подтверждения не найден в письме"
        return match.group(1)

@pytest.mark.environment("corp")
def test_change_email_and_confirm(auth_page: Page):
    """Тест смены email пользователя с подтверждением через код"""
    page = auth_page
    base_email = "ast123@mailforspam.com"
    new_email = "ast1233@mailforspam.com"
    initial_checkbox_state = None

    try:
        # --- Подготовка: включаем чекбокс если нужно ---
        page.get_by_role("link", name="Администрирование").click()
        page.get_by_role("link", name="Системные настройки").click()

        # Запоминаем исходное состояние чекбокса
        initial_checkbox_state = get_checkbox_state(page)

        # Включаем чекбокс, если он выключен
        toggle_checkbox_safe(page, enable=True)
        page.get_by_role("button", name="Сохранить").click()

        # Выход из админки
        page.get_by_role("link", name="Андрей Роднищев").click()
        page.get_by_role("link", name="Выход").click()

        # --- Основной тест смены почты ---
        # Логин под базовым пользователем
        page.get_by_role("textbox", name="Email или Логин").click()
        page.get_by_role("textbox", name="Email или Логин").fill(base_email)
        page.get_by_role("textbox", name="Пароль").click()
        page.get_by_role("textbox", name="Пароль").fill("1")
        page.get_by_role("button", name="Вход").click()

        # Переход в профиль и смена email
        page.get_by_role("link", name="Мой ассистент").click()
        page.get_by_role("link", name="Профиль").click()
        page.get_by_role("link", name=base_email).nth(0).click()
        page.locator("#Email").fill(new_email)
        page.get_by_role("button", name="Сохранить").click()
        expect(page.get_by_text("Введите код подтверждения")).to_be_visible(timeout=10000)

        # Получаем код подтверждения
        code = get_confirmation_code(page, new_email.split("@")[0])

        # Вводим код
        page.get_by_role("textbox", name="Введите код подтверждения").fill(code)
        page.get_by_role("button", name="Сохранить").click()
        expect(page.locator(".toast-message", has_text="Адрес электронной почты изменен")).to_be_visible(timeout=5000)

        # --- Логин под новой почтой ---
        page.get_by_role("textbox", name="Email или Логин").fill(new_email)
        page.get_by_role("textbox", name="Пароль").fill("1")
        page.get_by_role("button", name="Вход").click()

        # Переход в профиль и смена обратно на старую почту
        page.get_by_role("link", name=new_email).click()
        page.locator("#Email").click()
        page.locator("#Email").fill(base_email)
        page.get_by_role("button", name="Сохранить").click()
        expect(page.get_by_text("Введите код подтверждения")).to_be_visible(timeout=10000)

        # Получаем код для возврата
        code2 = get_confirmation_code(page, base_email.split("@")[0])

        # Вводим код
        page.get_by_role("textbox", name="Введите код подтверждения").fill(code2)
        page.get_by_role("button", name="Сохранить").click()
        expect(page.locator(".toast-message", has_text="Адрес электронной почты изменен")).to_be_visible(timeout=5000)

    finally:
        # --- Восстановление состояния ---
        try:
            # Попытка найти пользовательскую ссылку
            try:
                user_link = page.get_by_role("listitem").filter(has_text=f"{base_email} ast123")
                user_link.get_by_role("link").wait_for(state="visible", timeout=10000)
                user_link.get_by_role("link").click()
            except Exception:
                print("Пользовательская ссылка не найдена, пропускаем к логину админа")

            # Логин админа и восстановление состояния чекбокса
            page.get_by_role("textbox", name="Email или Логин").click()
            page.get_by_role("textbox", name="Email или Логин").fill("rodnischev@safib.ru")
            page.get_by_role("textbox", name="Пароль").click()
            page.get_by_role("textbox", name="Пароль").fill("1")
            page.get_by_role("button", name="Вход").click()

            page.get_by_role("link", name="Администрирование").click()
            page.get_by_role("link", name="Системные настройки").click()

            if initial_checkbox_state is not None:
                current_state = get_checkbox_state(page)
                if current_state != initial_checkbox_state:
                    toggle_checkbox_safe(page, enable=initial_checkbox_state)
                    page.get_by_role("button", name="Сохранить").click()

        except Exception as e:
            print(f"Ошибка при восстановлении состояния: {e}")