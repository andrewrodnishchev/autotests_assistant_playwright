import pytest
from playwright.sync_api import expect

def test_change_access_policy(auth_page):
    page = auth_page

    # Переход в нужную организацию
    page.get_by_role("link", name="тест андрей").click()
    page.wait_for_timeout(1000)

    # Переход на вкладку "Устройства"
    page.get_by_role("link", name="Устройства").click()
    page.wait_for_timeout(1000)

    # Выделяем два нужных устройства по строкам с частичным совпадением имени
    page.get_by_role("row", name="014 917 927").get_by_role("checkbox").check()
    page.get_by_role("row", name="135 026 892").get_by_role("checkbox").check()

    # Нажатие на иконку редактирования
    page.get_by_role("button", name="").click()
    page.wait_for_timeout(1000)

    # Кликаем по заголовку департамента "Не изменять"
    page.get_by_title("Не изменять", exact=True).click()

    # Выбираем из списка элемент <li> с текстом "фильтры тест"
    page.locator('li.select2-results__option', has_text="фильтры тест").click()
    page.wait_for_timeout(500)

    # Подтверждение изменений
    page.get_by_role("button", name="Выполнить").click()

    # Проверка уведомления об успехе
    toast = page.locator("div").filter(has_text="Успешно изменено устройств:")
    expect(toast.nth(1)).to_be_visible(timeout=5000)

    # Клик по фильтру "тест"
    page.get_by_text("фильтры тест").click()
    page.wait_for_timeout(1000)

    # Снятие всех галочек
    page.evaluate("document.querySelector('#DeviceTableNew_90-no-chkAll-btn').click()")
    page.wait_for_timeout(1000)

    # Нажатие на иконку редактирования
    page.get_by_role("button", name="").click()
    page.wait_for_timeout(1000)

    # Клик по заголовку департамента "Не изменять"
    page.get_by_title("Не изменять", exact=True).click()

    # Снова выбираем "фильтры тест" из списка
    page.locator('li.select2-results__option', has_text="фильтры тест").click()
    page.wait_for_timeout(500)

    # Подтверждение изменений
    page.get_by_role("button", name="Выполнить").click()
    page.wait_for_timeout(1000)

    # Проверка уведомления об успехе
    toast = page.locator("div").filter(has_text="Успешно изменено устройств:")
    expect(toast.nth(1)).to_be_visible(timeout=5000)

    # Снятие всех галочек
    page.locator("#DeviceTableNew_90-no-chkAll-btn").click()
    page.wait_for_timeout(1000)

    # Выделение всех устройств
    page.locator("#DeviceTableNew_90-chkAll-btn").click()
    page.wait_for_timeout(1000)

    # Повторное редактирование
    page.get_by_role("button", name="").click()
    page.wait_for_timeout(1000)

    # --- Выбор политики доступа "Базовая" ---
    policy_select = page.locator("div.SumoSelect.sumo_AccessPolicy")
    policy_select.click()
    page.wait_for_timeout(500)

    # Явный выбор первого варианта с текстом "Базовая"
    option = policy_select.locator("li.opt label", has_text="Базовая").first
    expect(option).to_be_visible(timeout=3000)
    option.click()
    page.wait_for_timeout(500)

    # Подтверждение изменений
    page.get_by_role("button", name="Выполнить").click()
    page.wait_for_timeout(1000)

    # Проверка повторного уведомления
    toast2 = page.locator("div").filter(has_text="Успешно изменено устройств:")
    expect(toast2.first).to_be_visible(timeout=5000)
