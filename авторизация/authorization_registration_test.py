import pytest
import time
from playwright.sync_api import expect, sync_playwright


@pytest.mark.parametrize("base_email", ["rodnischev"])
def test_register_new_user(base_email, playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    # Переход на страницу логина
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")

    # Проверяем наличие ссылки "Регистрация учетной записи"
    if not page.locator("text=Регистрация учетной записи").is_visible():
        # Если кнопки нет — заходим в админку и включаем регистрацию
        page.get_by_role("textbox", name="Email или Логин").fill("rodnischev@safib.ru")
        page.get_by_role("textbox", name="Пароль").fill("1")
        page.get_by_role("button", name="Вход").click()

        page.get_by_role("link", name="Администрирование").click()
        page.get_by_role("link", name="Системные настройки").click()

        # Кликаем по чекбоксу настройки регистрации
        page.locator("div:nth-child(3) > .col-sm-10 > .i-checks > .icheckbox_square-green > .iCheck-helper").first.click()

        # Нажимаем кнопку Сохранить
        page.locator("button.btn.btn-primary", has_text="Сохранить").click()

        # Проверяем, что настройки сохранены
        expect(page.locator("div.alert.alert-success")).to_be_visible(timeout=5000)

        # Выходим из аккаунта
        page.get_by_role("link", name="Андрей Роднищев").click()
        page.get_by_role("link", name="Выход").click()

        # Снова переходим на страницу логина
        page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")

    # Переходим на страницу регистрации
    page.get_by_role("link", name="Регистрация учетной записи").click()

    # Перебор почт до первой успешной регистрации
    for i in range(1, 50):
        email = f"{base_email}{i}@mailforspam.com"
        username = f"тест андрей {i}"

        page.get_by_role("textbox", name="Электронная почта").fill(email)
        page.get_by_role("textbox", name="Имя").fill(username)
        page.get_by_role("textbox", name="Пароль", exact=True).fill("1")
        page.get_by_role("textbox", name="Подтвердите пароль").fill("1")
        page.get_by_role("button", name="Зарегистрировать учетную запись").click()

        try:
            expect(page.get_by_text("Для завершения регистрации необходимо перейти по ссылке")).to_be_visible(timeout=3000)
            break
        except:
            continue
    else:
        pytest.fail("Не удалось зарегистрировать ни одну почту")

    # Переход в mailforspam
    confirm_page = context.new_page()
    confirm_page.goto("https://www.mailforspam.com/", wait_until="domcontentloaded")
    time.sleep(2)
    confirm_page.locator("#input_box").fill(f"{base_email}{i}")
    time.sleep(3)
    confirm_page.get_by_role("button", name="Check").click()

    # Ждём появления хотя бы одного письма с нужным названием
    expect(confirm_page.locator("a:has-text('Код подтверждения для завершения регистрации')").first).to_be_visible(timeout=10000)

    # Кликаем по самому новому письму
    confirm_page.locator("a:has-text('Код подтверждения для завершения регистрации')").first.click()

    confirm_page.get_by_role("link", name="ссылке").click()
    expect(confirm_page.get_by_text("Ваша учетная запись успешно активирована")).to_be_visible()

    # Авторизация
    confirm_page.get_by_role("link", name="Вход в личный кабинет").click()
    confirm_page.get_by_role("textbox", name="Email или Логин").fill(email)
    confirm_page.get_by_role("textbox", name="Пароль").fill("1")
    confirm_page.get_by_role("button", name="Вход").click()

    # Проверка перехода на нужную страницу
    confirm_page.wait_for_url("http://lk.corp.dev.ru/ClientDevice", timeout=5000)
    assert confirm_page.url == "http://lk.corp.dev.ru/ClientDevice", "Авторизация не удалась — редирект не выполнен"

    context.close()
    browser.close()
