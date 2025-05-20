from playwright.sync_api import expect
import pytest

def test_create_device_group_codegen_style(auth_page):
    page = auth_page
    base_group_name = "тест"
    max_attempts = 10

    # Открываем раздел "Мой ассистент" → "Устройства"
    page.get_by_role("link", name=" Мой ассистент ").click()
    page.get_by_role("link", name=" Устройства").click()

    # Открываем форму добавления группы
    page.get_by_role("link", name="Добавить группу").click()

    for attempt in range(1, max_attempts + 1):
        group_name = f"{base_group_name} {attempt}"

        # Заполняем поле с именем
        name_field = page.locator("#Name")
        name_field.fill("")  # очистка
        name_field.fill(group_name)

        # Нажимаем "Сохранить"
        save_button = page.get_by_role("button", name="Сохранить")
        save_button.click()
        save_button.click()  # как в оригинале

        try:
            # Проверка: есть ли сообщение об ошибке дубликата
            expect(page.get_by_text("Группа с таким наименованием уже существует")).to_be_visible(timeout=2000)
            print(f"⚠ Группа '{group_name}' уже существует, пробуем следующее имя...")
            continue
        except AssertionError:
            # Проверка: успешное создание
            page.get_by_text("Группа устройств успешно создана")
            return

    # Если все попытки неуспешны
    pytest.fail(f"❌ Не удалось создать уникальную группу за {max_attempts} попыток")
