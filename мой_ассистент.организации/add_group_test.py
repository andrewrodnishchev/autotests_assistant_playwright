from playwright.sync_api import expect
import pytest

def test_create_device_group(auth_page):
    page = auth_page
    base_group_name = "тест"
    max_attempts = 10

    # Переходим в нужные разделы
    page.get_by_role("link", name="тест андрей").click()
    page.get_by_role("link", name="Устройства").click()

    # Открываем форму создания группы
    page.get_by_title("Добавить группу").click()

    for attempt in range(1, max_attempts + 1):
        group_name = f"{base_group_name} {attempt}"

        # Заполняем имя группы
        name_field = page.locator("#Name")
        name_field.fill("")  # Очищаем поле
        name_field.fill(group_name)

        # Нажимаем сохранить (дважды, как в вашем примере)
        page.get_by_role("button", name="Сохранить").click()
        page.get_by_role("button", name="Сохранить").click()

        try:
            # Проверяем сообщение о дубликате
            expect(page.get_by_text("Группа с таким наименованием уже существует")).to_be_visible(timeout=2000)
            print(f"Группа '{group_name}' уже существует, пробуем следующее имя")

            # Если группа существует, продолжаем цикл со следующим номером
            continue
        except AssertionError:
            # Если дубликата нет - проверяем успешное создание
            expect(page.get_by_text("Группа устройств успешно создана")).to_be_visible()
            print(f"Успешно создана группа: '{group_name}'")
            return

    pytest.fail(f"Не удалось создать группу после {max_attempts} попыток")