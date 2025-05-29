import pytest
import time
import os
from typing import Optional
from playwright.sync_api import Browser, Page, expect

# Статистика тестов
passed_tests = []
failed_tests = []
skipped_tests = []
test_durations = {}
session_start_time: Optional[float] = None
test_start_times = {}

# ---------- Фикстура авторизации ----------

@pytest.fixture
def auth_page(browser: Browser) -> Page:
    """Изолированная фикстура: авторизация в новом браузерном контексте."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        screen={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    page.set_default_timeout(45_000)

    try:
        page.goto("http://lk.corp.dev.ru/Account/Login?returnUrl=%2FClientOrg")

        page.get_by_role("textbox", name="Email или Логин").fill("rodnischev@safib.ru")
        page.get_by_role("textbox", name="Пароль").fill("1")
        page.get_by_role("button", name="Вход").click()

        expect(page).not_to_have_url("http://lk.corp.dev.ru/Account/Login", timeout=5000)

        yield page
    except Exception as e:
        pytest.fail(f"Авторизация не удалась: {e}")
    finally:
        context.close()


# ---------- Параметры запуска браузера ----------

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Аргументы запуска браузера: включаем полноэкранный режим и headful."""
    slow_mo_value = int(os.getenv("SLOWMO", "0"))
    return {
        "headless": False,
        "args": ["--start-fullscreen"],
        "slow_mo": slow_mo_value
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """Параметры контекста браузера — задаём размер экрана."""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "screen": {"width": 1920, "height": 1080}
    }


# ---------- Хуки pytest ----------

def pytest_sessionstart(session):
    global session_start_time
    session_start_time = time.time()


def pytest_runtest_protocol(item, nextitem):
    test_name = item.nodeid
    test_start_times[test_name] = time.time()
    return None


def pytest_runtest_logreport(report):
    if report.when != "call":
        return

    test_name = report.nodeid
    start_time = test_start_times.get(test_name, time.time())
    duration = time.time() - start_time
    test_durations[test_name] = duration

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    if report.passed:
        passed_tests.append(test_name)
        print(f"{GREEN}✔ {test_name} PASSED [{duration:.2f}s]{RESET}")

    elif report.failed:
        failed_tests.append(test_name)
        print(f"{RED}✘ {test_name} FAILED [{duration:.2f}s]{RESET}")
        if hasattr(report, "longrepr"):
            print(f"{RED}  Ошибка:{RESET}")
            for line in str(report.longrepr).splitlines():
                print(f"{RED}    {line}{RESET}")

    elif report.skipped:
        skipped_tests.append(test_name)
        print(f"{YELLOW}⚠ {test_name} SKIPPED{RESET}")


def pytest_sessionfinish(session, exitstatus):
    session_end_time = time.time()
    total_duration = session_end_time - session_start_time

    print("\n========== РЕЗУЛЬТАТЫ ТЕСТОВ ==========")

    if passed_tests:
        print("\033[92m✅ PASSED:\033[0m")
        for name in passed_tests:
            print(f"  ✔ {name} [{test_durations.get(name, 0):.2f}s]")

    if failed_tests:
        print("\033[91m❌ FAILED:\033[0m")
        for name in failed_tests:
            print(f"  ✘ {name} [{test_durations.get(name, 0):.2f}s]")

    if skipped_tests:
        print("\033[93m⚠ SKIPPED:\033[0m")
        for name in skipped_tests:
            print(f"  ⚠ {name}")

    print(f"\n⏱ Общее время выполнения: {total_duration:.2f} секунд")
    print("==========================================")
