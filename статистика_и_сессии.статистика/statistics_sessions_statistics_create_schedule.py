import pytest
import time
from playwright.sync_api import expect


def test_chart_interaction(auth_page):
    page = auth_page
    timeout = 10_000

    # Переход в раздел "Статистика"
    page.get_by_role("link", name=" Статистика и сессии ").click()
    page.get_by_role("link", name=" Статистика").click()

    # Нажимаем "Сформировать график"
    page.get_by_role("button", name="Сформировать график").click()

    # Ожидание появления canvas-графика
    chart = page.locator("canvas")
    chart.wait_for(timeout=timeout)
    time.sleep(3)
    # Проверяем наличие графика
    expect(chart).to_be_visible()

    # Кликаем по графику в нескольких точках
    chart.click(position={"x": 286, "y": 74})
    time.sleep(0.5)
    chart.click(position={"x": 442, "y": 169})
    time.sleep(1)
