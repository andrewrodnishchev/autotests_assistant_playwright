from playwright.sync_api import Page, expect

def login(page: Page, email: str, password: str = "1"):
    page.get_by_role("textbox", name="Email или Логин").click()
    page.get_by_role("textbox", name="Email или Логин").fill(email)
    page.get_by_role("textbox", name="Пароль").click()
    page.get_by_role("textbox", name="Пароль").fill(password)
    page.get_by_role("button", name="Вход").click()
    expect(page).not_to_have_url("http://lk.corp.dev.ru/Account/Login", timeout=5000)

def test_org_exit_and_reactivate(page: Page):
    # Логин под ast123@mailforspam.com
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")
    login(page, "ast123@mailforspam.com")

    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Профиль").click()
    page.get_by_role("link", name="Мои организации", exact=True).click()
    page.get_by_role("gridcell", name="тест андрей").click(button="right")
    page.get_by_role("link", name="Выйти из организации").click()
    page.get_by_role("button", name="Выйти").click()
    page.locator("div").filter(has_text="Вы успешно вышли из организации").nth(1).click()
    page.get_by_role("link", name="ast123@mailforspam.com").click()
    page.get_by_role("link", name="Выход").click()

    # Логин под rodnischev@safib.ru
    page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")
    login(page, "rodnischev@safib.ru")

    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Сотрудники").click()
    page.get_by_role("gridcell", name="ast123@mailforspam.com").first.click(button="right")
    page.get_by_role("link", name="Активировать", exact=True).click()
    page.get_by_role("button", name="Активировать").click()
    page.locator("div").filter(has_text="Сотрудник успешно активирован").nth(1).click()
