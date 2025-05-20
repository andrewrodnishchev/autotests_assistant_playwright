from playwright.sync_api import Page

def test_activate_license_from_device_list(auth_page: Page):
    page = auth_page

    # 1. Упрощенный переход в раздел устройств
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # 2. Клик ПКМ по устройству
    device_cell = page.get_by_role("gridcell", name="000 000")
    device_cell.click(button="right")

    # 3. Выбор пункта меню
    page.get_by_role("link", name="Активировать лицензию").click()

    # 4. Выбор лицензии
    page.get_by_role("button", name="По умолчанию1 По умолчанию").click()
    page.locator("label", has_text="тест андрей CB71353D-619BEC40-8076D68A-FF302886").click()

    # 5. Основной клик на кнопку "Активировать" с улучшениями
    activate_btn = page.get_by_role("button", name="Активировать")

    # Способ 1: Обычный клик
    try:
        activate_btn.click()
    except:
        # Способ 2: Клик через JavaScript
        page.evaluate('(element) => element.click()', activate_btn.element_handle())

    # 6. Проверка сообщения (упрощенный вариант)
    success_message = page.locator("div").filter(has_text="Лицензия успешно активирована").nth(1)
    success_message.wait_for(timeout=10000)  # Ждем до 10 секунд
    success_message.click()

    # 7. Вторая часть теста (без изменений)
    page.get_by_role("row", name="   001 000 000 c405-Andrey").get_by_role("checkbox").check()
    page.get_by_role("button", name="").click()
    page.get_by_role("button", name="Активировать").click()

    success_message2 = page.locator("div").filter(
        has_text="Лицензия успешно активирована на выбранных устройствах (1 шт.)"
    ).nth(1)
    success_message2.wait_for()
    success_message2.click()

