import pytest
import time
import os
import platform
from typing import Dict, Any, List, Optional
from playwright.sync_api import Browser, Page, expect

# ---------- Конфигурация окружений ----------
ENVIRONMENTS: Dict[str, Dict[str, Any]] = {
    'corp': {
        'base_url': 'http://lk.corp.dev.ru',
        'login': 'rodnischev@safib.ru',
        'password': '1',
        'timeout': 45000
    },
    'setup': {
        'base_url': 'http://office.setuplk.ru',
        'login': 'rodnischev@safib.ru',
        'password': '1',
        'timeout': 45000
    }
}

# ---------- Глобальные переменные ----------
REPORTS_DIR = "test_reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

class TestState:
    def __init__(self):
        self.passed_tests: List[str] = []
        self.failed_tests: List[str] = []
        self.skipped_tests: List[str] = []
        self.test_durations: Dict[str, float] = {}
        self.test_start_times: Dict[str, float] = {}
        self.session_start_time: float = 0
        self.report_data: Optional[Dict[str, Any]] = None
        self.total_tests = 0
        self.completed_tests = 0
        self.config = None
        self.test_status_history: List[str] = []
        self.active_tests: Dict[str, str] = {}
        self.last_printed_line_length = 0
        self.current_test_number = 0

test_state = TestState()

# ---------- Цвета для консоли ----------
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    YELLOW = "\033[93m"

def clear_line():
    """Очищает текущую строку в консоли"""
    print("\r" + " " * (test_state.last_printed_line_length or 80) + "\r", end="")

def print_test_result(test_name: str, status: str, duration: float = 0.0):
    """Выводит результат выполнения теста с прогресс-баром"""
    clear_line()

    # Обновляем статус теста
    if status == "running":
        test_state.active_tests[test_name] = "running"
    else:
        if test_name in test_state.active_tests:
            test_state.active_tests.pop(test_name)
        test_state.test_status_history.append(status)

    # Адаптивная длина прогресс-бара
    max_bar_length = min(80, max(50, test_state.total_tests))
    bar_length = min(max_bar_length, test_state.total_tests)

    # Рассчитываем пропорции для отображения
    total_shown = min(bar_length, len(test_state.test_status_history) + len(test_state.active_tests))
    passed = len([s for s in test_state.test_status_history if s == "passed"])
    failed = len([s for s in test_state.test_status_history if s == "failed"])
    skipped = len([s for s in test_state.test_status_history if s == "skipped"])
    active = len(test_state.active_tests)

    # Создаем прогресс-бар
    bar_parts = []
    bar_parts.extend([f"{Colors.GREEN}█"] * passed)
    bar_parts.extend([f"{Colors.RED}█"] * failed)
    bar_parts.extend([f"{Colors.YELLOW}█"] * skipped)
    bar_parts.extend([f"{Colors.CYAN}▒"] * active)

    # Обрезаем до нужной длины и добавляем оставшиеся
    bar_parts = bar_parts[:bar_length]
    remaining = bar_length - len(bar_parts)
    if remaining > 0:
        bar_parts.append(f"{Colors.GRAY}{'░' * remaining}")

    bar = "".join(bar_parts) + Colors.RESET

    # Определяем цвет и иконку статуса
    if status == "passed":
        color = Colors.GREEN
        status_icon = "✓"
    elif status == "failed":
        color = Colors.RED
        status_icon = "✘"
    elif status == "running":
        color = Colors.CYAN
        status_icon = "⌛"
    else:
        color = Colors.YELLOW
        status_icon = "↷"

    # Формируем строку вывода
    test_line = (
        f"Тест {test_state.current_test_number}/{test_state.total_tests} |{bar}| "
        f"{color}{status_icon} {test_name.split('::')[-1][:40]}{Colors.RESET}"
    )

    if status != "running":
        test_line += f" ({duration:.2f} сек)"

    # Сохраняем длину строки для очистки
    test_state.last_printed_line_length = len(
        test_line.replace(Colors.GREEN, "")
        .replace(Colors.RED, "")
        .replace(Colors.YELLOW, "")
        .replace(Colors.CYAN, "")
        .replace(Colors.GRAY, "")
        .replace(Colors.RESET, "")
    )

    print(test_line, end="", flush=True)

    if status != "running":
        print()  # Переход на новую строку для завершенных тестов
        if status == "failed":
            error_msg = str(test_state.report_data['tests'][-1]['error']).split('\n')[0][:200] if test_state.report_data and test_state.report_data['tests'] else ""
            print(f"{Colors.RED}   Ошибка: {error_msg}...{Colors.RESET}")
            if test_state.report_data and test_state.report_data['tests'] and test_state.report_data['tests'][-1].get("screenshot"):
                print(f"{Colors.BLUE}   Скриншот: {test_state.report_data['tests'][-1]['screenshot']}{Colors.RESET}")
        elif status == "skipped":
            skip_msg = str(test_state.report_data['tests'][-1]['error']).split('\n')[0][:200] if test_state.report_data and test_state.report_data['tests'] and test_state.report_data['tests'][-1].get('error') else "Тест пропущен"
            print(f"{Colors.YELLOW}   Причина: {skip_msg}...{Colors.RESET}")
            if test_state.report_data and test_state.report_data['tests'] and test_state.report_data['tests'][-1].get("screenshot"):
                print(f"{Colors.BLUE}   Скриншот: {test_state.report_data['tests'][-1]['screenshot']}{Colors.RESET}")
        print(f"{Colors.GRAY}{'─' * 80}{Colors.RESET}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    item.closed_browser = False
    yield
    if hasattr(item, "_request") and hasattr(item._request, "fixturenames"):
        if "page" in item._request.fixturenames:
            try:
                page = item._request.getfixturevalue("page")
                if page.is_closed():
                    item.closed_browser = True
            except:
                item.closed_browser = True

@pytest.fixture(scope="session")
def browser_type_launch_args() -> Dict[str, Any]:
    return {
        "headless": False,
        "args": ["--start-fullscreen"],
        "slow_mo": int(os.getenv("SLOWMO", "0"))
    }

@pytest.fixture(scope="session")
def browser_context_args() -> Dict[str, Any]:
    return {
        "viewport": {"width": 1920, "height": 1080},
        "screen": {"width": 1920, "height": 1080}
    }

@pytest.fixture
def auth_page(browser: Browser, request: pytest.FixtureRequest) -> Page:
    env = get_current_environment(request)
    config = ENVIRONMENTS[env]

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        screen={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    page.set_default_timeout(config['timeout'])

    try:
        login_url = f"{config['base_url']}/Account/Login?returnUrl=%2FClientOrg"
        page.goto(login_url)

        locator = page.get_by_role("textbox", name="Email или Логин")
        if not locator.is_visible(timeout=2000):
            locator = page.get_by_role("textbox", name="Email")

        locator.fill(config['login'])
        page.get_by_role("textbox", name="Пароль").fill(config['password'])
        page.get_by_role("button", name="Вход").click()
        expect(page).not_to_have_url(login_url, timeout=5000)
        yield page
    except Exception as e:
        if request.node.closed_browser:
            pytest.skip("Тест прерван пользователем (браузер закрыт)")
        else:
            screenshot_path = os.path.join(REPORTS_DIR, f"error_{time.strftime('%H%M%S')}.png")
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                pytest.fail(f"Ошибка теста ({env}): {str(e)[:200]}...\nСкриншот: {screenshot_path}")
            except:
                pytest.fail(f"Ошибка теста ({env}): {str(e)[:200]}")
    finally:
        try:
            context.close()
        except:
            pass

def get_current_environment(request: pytest.FixtureRequest) -> str:
    env_marker = request.node.get_closest_marker("environment")
    if env_marker and len(env_marker.args) > 0 and env_marker.args[0] in ENVIRONMENTS:
        return env_marker.args[0]

    env_arg = request.config.getoption("--env")
    if env_arg and env_arg in ENVIRONMENTS:
        return env_arg

    return 'corp'

def get_system_info() -> Dict[str, str]:
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
        "system_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env", choices=list(ENVIRONMENTS.keys()), default='corp',
        help="Выбор окружения для тестов: corp или setup"
    )
    parser.addoption(
        "--report-format", choices=["html", "none"], default="html",
        help="Формат отчета: html или none"
    )
    parser.addoption(
        "--screenshots", action="store_true", default=False,
        help="Сохранять скриншоты для упавших тестов"
    )

def pytest_configure(config: pytest.Config) -> None:
    config.option.progress = 'no'
    config.option.verbose = 0
    config.option.quiet = True

    test_state.config = config
    test_state.report_data = {
        "env": config.getoption("--env"),
        "start_time": time.time(),
        "system": get_system_info(),
        "tests": [],
        "stats": {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "total": 0
        },
        "screenshots": {}
    }

def pytest_sessionstart(session: pytest.Session) -> None:
    test_state.session_start_time = time.time()
    print(f"\n{Colors.BLUE}╔════════════════════════╗")
    print(f"║ {Colors.BOLD}{Colors.WHITE}🚀 НАЧАЛО ТЕСТИРОВАНИЯ {Colors.RESET}{Colors.BLUE}║")
    print(f"╚════════════════════════╝{Colors.RESET}\n")

def pytest_collection_modifyitems(session: pytest.Session, config: pytest.Config, items: List[pytest.Item]) -> None:
    test_state.total_tests = len(items)
    test_state.completed_tests = 0
    print(f"{Colors.CYAN}• Всего тестов: {test_state.total_tests}{Colors.RESET}")
    print(f"{Colors.CYAN}• Окружение: {config.getoption('--env')}{Colors.RESET}")
    print(f"{Colors.CYAN}• Отчет: {config.getoption('--report-format')}{Colors.RESET}\n")
    print(f"{Colors.GRAY}{'─' * 80}{Colors.RESET}")

def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    if not test_state.report_data:
        return

    test_name = report.nodeid.split("::")[-1]

    if report.when == "setup":
        test_state.test_start_times[test_name] = time.time()
        test_state.current_test_number = test_state.completed_tests + 1
        print_test_result(
            test_name=report.nodeid,
            status="running"
        )
        return

    duration = time.time() - test_state.test_start_times.get(test_name, time.time())
    test_state.test_durations[test_name] = duration

    if report.when == "call":
        test_state.completed_tests += 1

    test_data = {
        "name": test_name,
        "duration": duration,
        "status": report.outcome,
        "error": None,
        "screenshot": None,
        "when": report.when
    }

    if report.when == "call":
        if hasattr(report, "closed_browser") and report.closed_browser:
            report.outcome = "skipped"
            test_data["status"] = "skipped"
            test_data["error"] = "Тест прерван пользователем (браузер закрыт)"

        if report.outcome == "failed":
            test_state.failed_tests.append(test_name)
            test_state.report_data["stats"]["failed"] += 1
            if report.longrepr and "Скриншот:" in str(report.longrepr):
                test_data["screenshot"] = str(report.longrepr).split("Скриншот:")[-1].strip()
            test_data["error"] = str(report.longrepr)[:500] if report.longrepr else None

        elif report.outcome == "passed":
            test_state.passed_tests.append(test_name)
            test_state.report_data["stats"]["passed"] += 1

        elif report.outcome == "skipped":
            test_state.skipped_tests.append(test_name)
            test_state.report_data["stats"]["skipped"] += 1
            if report.longrepr:
                test_data["error"] = str(report.longrepr)[:500]
                if "Скриншот:" in str(report.longrepr):
                    test_data["screenshot"] = str(report.longrepr).split("Скриншот:")[-1].strip()

        test_state.report_data["stats"]["total"] += 1
        test_state.report_data["tests"].append(test_data)

        print_test_result(
            test_name=report.nodeid,
            status=report.outcome,
            duration=duration
        )

def pytest_runtest_setup(item: pytest.Item) -> None:
    test_name = item.nodeid.split("::")[-1]
    test_state.test_start_times[test_name] = time.time()

def pytest_sessionfinish(session: pytest.Session, exitstatus: pytest.ExitCode) -> None:
    if not test_state.report_data:
        return

    total_duration = time.time() - test_state.session_start_time
    test_state.report_data["total_duration"] = total_duration
    test_state.report_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    total = test_state.report_data["stats"]["total"]
    passed = test_state.report_data["stats"]["passed"]
    passed_percent = round((passed / total) * 100, 1) if total > 0 else 0
    test_state.report_data["stats"]["passed_percent"] = passed_percent

    if test_state.config.getoption("--report-format") == "html":
        generate_html_report(test_state.report_data)
        report_files = [f for f in os.listdir(REPORTS_DIR) if f.startswith("report_") and f.endswith(".html")]
        if report_files:
            report_file = report_files[-1]
            print(f"\n{Colors.BLUE}• Отчет сохранен: {os.path.join(REPORTS_DIR, report_file)}{Colors.RESET}")

    print(f"\n{Colors.BLUE}╔═══════════════════════╗")
    print(f"║ {Colors.BOLD}{Colors.WHITE}📊 ИТОГИ ТЕСТИРОВАНИЯ {Colors.RESET}{Colors.BLUE}║")
    print(f"╚═══════════════════════╝{Colors.RESET}")

    print(f"{Colors.CYAN}┌{'─' * 78}┐{Colors.RESET}")
    print(f"{Colors.CYAN}│ {Colors.BOLD}Всего тестов:{Colors.RESET} {total}{' ' * (62 - len(str(total)))} {Colors.CYAN}│")
    print(f"{Colors.CYAN}│ {Colors.GREEN}✓ Пройдено:  {Colors.RESET}{passed} ({passed_percent}%){' ' * (60 - len(f'{passed} ({passed_percent}%)'))}    {Colors.CYAN}│")
    print(f"{Colors.CYAN}│ {Colors.RED}✘ Провалено: {Colors.RESET}{test_state.report_data['stats']['failed']}{' ' * (62 - len(str(test_state.report_data['stats']['failed'])))}  {Colors.CYAN}│")
    print(f"{Colors.CYAN}│ {Colors.YELLOW}↷ Пропущено: {Colors.RESET}{test_state.report_data['stats']['skipped']}{' ' * (62 - len(str(test_state.report_data['stats']['skipped'])))}  {Colors.CYAN}│")
    print(f"{Colors.CYAN}│ {Colors.BOLD}Общее время:{Colors.RESET} {total_duration:.2f} сек{' ' * (60 - len(f'{total_duration:.2f} сек'))}    {Colors.CYAN}│")
    print(f"{Colors.CYAN}│ {Colors.BOLD}Окружение: {Colors.RESET}{test_state.report_data['env']}{' ' * (62 - len(test_state.report_data['env']))}    {Colors.CYAN}│")
    print(f"{Colors.CYAN}└{'─' * 78}┘{Colors.RESET}")

    if test_state.failed_tests:
        print(f"\n{Colors.RED}╔═════════════════════╗")
        print(f"║ {Colors.BOLD}{Colors.WHITE}❌ ПРОВАЛЕННЫЕ ТЕСТЫ {Colors.RESET}{Colors.RED}║")
        print(f"╚═════════════════════╝{Colors.RESET}")

        for name in test_state.failed_tests:
            test_data = next((t for t in test_state.report_data["tests"] if t["name"] == name and t["when"] == "call"), {})
            print(f"\n{Colors.RED}✘ {name}{Colors.RESET}")
            if test_data.get("error"):
                print(f"{Colors.GRAY}   Ошибка: {test_data['error'].split('\n')[0][:200]}...{Colors.RESET}")
            if test_data.get("screenshot"):
                print(f"{Colors.BLUE}   Скриншот: {test_data['screenshot']}{Colors.RESET}")
            print(f"{Colors.GRAY}{'─' * 80}{Colors.RESET}")

    if test_state.skipped_tests:
        print(f"\n{Colors.YELLOW}╔════════════════════════════╗")
        print(f"║ {Colors.BOLD}{Colors.WHITE}⚠ ПРОПУЩЕННЫЕ ТЕСТЫ {Colors.RESET}{Colors.YELLOW}║")
        print(f"╚════════════════════════════╝{Colors.RESET}")

        for name in test_state.skipped_tests:
            test_data = next((t for t in test_state.report_data["tests"] if t["name"] == name and t["when"] == "call"), {})
            print(f"\n{Colors.YELLOW}↷ {name}{Colors.RESET}")
            if test_data.get("error"):
                print(f"{Colors.GRAY}   Причина: {test_data['error'].split('\n')[0][:200]}...{Colors.RESET}")
            print(f"{Colors.GRAY}{'─' * 80}{Colors.RESET}")

    print(f"\n{Colors.BLUE}╔═══════════════════════════╗")
    print(f"║ {Colors.BOLD}{Colors.WHITE}✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО {Colors.RESET}{Colors.BLUE}║")
    print(f"╚═══════════════════════════╝{Colors.RESET}\n")

def generate_html_report(report_data: Dict[str, Any]) -> None:
    filename = os.path.join(REPORTS_DIR, f"report_{time.strftime('%Y%m%d_%H%M%S')}.html")

    # Подготовка данных для графика
    passed = report_data['stats']['passed']
    failed = report_data['stats']['failed']
    skipped = report_data['stats']['skipped']
    total = report_data['stats']['total']

    passed_percent = report_data['stats']['passed_percent']
    failed_percent = round((failed / total) * 100, 1) if total > 0 else 0
    skipped_percent = round((skipped / total) * 100, 1) if total > 0 else 0

    # Формирование строк таблицы
    test_rows = []
    for i, test in enumerate([t for t in report_data["tests"] if t["when"] == "call"]):
        status_icon = ""
        if test["status"] == "passed":
            status_icon = '<span class="status-icon">✓</span>'
        elif test["status"] == "failed":
            status_icon = '<span class="status-icon">✘</span>'
        else:
            status_icon = '<span class="status-icon">↷</span>'

        screenshot_html = ""
        if test.get("screenshot"):
            screenshot_name = os.path.basename(test["screenshot"])
            screenshot_html = f"""
                <div class="screenshot-container">
                    <a href="{test['screenshot']}" class="screenshot-link" target="_blank">
                        <img src="{test['screenshot']}" alt="Скриншот ошибки" class="screenshot-thumb">
                        <span>Просмотр скриншота</span>
                    </a>
                </div>
            """

        error_html = ""
        if test.get("error"):
            if test["status"] == "failed":
                error_html = f'<div class="error-details">{test["error"]}</div>'
            elif test["status"] == "skipped":
                error_html = f'<div class="skip-details">{test["error"]}</div>'

        test_rows.append(f"""
        <tr class="test-row {test["status"]}-row">
            <td>{i+1}</td>
            <td>{test["name"]}</td>
            <td class="status-cell">
                <span class="status-badge {test["status"]}">
                    {status_icon} {test["status"].upper()}
                </span>
            </td>
            <td class="duration-cell">{test["duration"]:.2f} сек</td>
            <td class="details-cell">
                {error_html}
                {screenshot_html}
            </td>
        </tr>
        """)

    test_rows_html = "".join(test_rows)

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Отчет о тестировании | Playwright + Pytest</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {{
                --primary: #3498db;
                --primary-dark: #2980b9;
                --success: #2ecc71;
                --success-dark: #27ae60;
                --danger: #e74c3c;
                --danger-dark: #c0392b;
                --warning: #f39c12;
                --warning-dark: #d35400;
                --info: #3498db;
                --light: #f8f9fa;
                --dark: #343a40;
                --gray: #6c757d;
                --light-gray: #e9ecef;
                --border: #dee2e6;
                --shadow: rgba(0, 0, 0, 0.1);
            }}
            
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f8f9fa;
                margin: 0;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 5px 25px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            
            /* Шапка отчета */
            header {{
                background: linear-gradient(135deg, #2c3e50, #1a2530);
                color: white;
                padding: 40px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            header::before {{
                content: "";
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
                pointer-events: none;
            }}
            
            .header-content {{
                position: relative;
                z-index: 1;
            }}
            
            h1 {{
                font-size: 2.8rem;
                margin-bottom: 10px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }}
            
            .subtitle {{
                font-size: 1.2rem;
                opacity: 0.9;
                margin-bottom: 20px;
            }}
            
            .report-meta {{
                display: flex;
                justify-content: center;
                gap: 30px;
                margin-top: 25px;
                flex-wrap: wrap;
            }}
            
            .meta-item {{
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 1.1rem;
            }}
            
            .meta-item i {{
                font-size: 1.4rem;
                color: #3498db;
            }}
            
            /* Сводная статистика */
            .summary-stats {{
                display: flex;
                justify-content: space-between;
                padding: 30px 40px;
                background-color: #fff;
                border-bottom: 1px solid var(--border);
                flex-wrap: wrap;
            }}
            
            .summary-item {{
                text-align: center;
                flex: 1;
                min-width: 200px;
                padding: 15px;
            }}
            
            .summary-item h3 {{
                font-size: 1.2rem;
                color: var(--gray);
                margin-bottom: 10px;
                font-weight: 500;
            }}
            
            .summary-item .value {{
                font-size: 2.2rem;
                font-weight: 700;
                margin: 10px 0;
            }}
            
            .summary-item .value.passed {{ color: var(--success); }}
            .summary-item .value.failed {{ color: var(--danger); }}
            .summary-item .value.skipped {{ color: var(--warning); }}
            .summary-item .value.duration {{ color: var(--primary); }}
            
            /* Карточки статистики */
            .stats-section {{
                padding: 30px 40px;
                background-color: #f0f4f8;
            }}
            
            .stats-title {{
                text-align: center;
                font-size: 1.8rem;
                margin-bottom: 30px;
                color: var(--dark);
                position: relative;
            }}
            
            .stats-title::after {{
                content: "";
                display: block;
                width: 80px;
                height: 4px;
                background: var(--primary);
                margin: 10px auto;
                border-radius: 2px;
            }}
            
            .stats-cards {{
                display: flex;
                justify-content: center;
                gap: 25px;
                flex-wrap: wrap;
            }}
            
            .stat-card {{
                flex: 1;
                min-width: 250px;
                max-width: 300px;
                padding: 30px 20px;
                border-radius: 12px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }}
            
            .stat-card::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
            }}
            
            .stat-card.total {{ 
                background: linear-gradient(135deg, #3498db, #0D47A1); 
            }}
            
            .stat-card.total::before {{ background: #0D47A1; }}
            
            .stat-card.passed {{ 
                background: linear-gradient(135deg, #2ecc71, #27ae60); 
            }}
            
            .stat-card.passed::before {{ background: #27ae60; }}
            
            .stat-card.failed {{ 
                background: linear-gradient(135deg, #e74c3c, #c0392b); 
            }}
            
            .stat-card.failed::before {{ background: #c0392b; }}
            
            .stat-card.skipped {{ 
                background: linear-gradient(135deg, #f39c12, #e67e22); 
            }}
            
            .stat-card.skipped::before {{ background: #e67e22; }}
            
            .stat-card h3 {{
                font-size: 3.2rem;
                margin-bottom: 10px;
                font-weight: 700;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            
            .stat-card p {{
                font-size: 1.3rem;
                opacity: 0.9;
                margin-top: 5px;
            }}
            
            /* Прогресс-бар */
            .progress-section {{
                padding: 30px 40px;
                background: white;
            }}
            
            .progress-header {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 15px;
                align-items: center;
            }}
            
            .progress-title {{
                font-size: 1.4rem;
                font-weight: 600;
                color: var(--dark);
            }}
            
            .progress-percent {{
                font-size: 1.8rem;
                font-weight: 700;
                color: var(--success);
            }}
            
            .progress-bar-container {{
                height: 28px;
                background-color: var(--light-gray);
                border-radius: 14px;
                overflow: hidden;
                position: relative;
                box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
            }}
            
            .progress-bar {{
                height: 100%;
                background: linear-gradient(90deg, var(--success), var(--success-dark));
                border-radius: 14px;
                width: {passed_percent}%;
                position: relative;
                transition: width 1s ease-in-out;
            }}
            
            .progress-labels {{
                display: flex;
                justify-content: space-between;
                margin-top: 10px;
                font-size: 0.95rem;
                color: var(--gray);
            }}
            
            /* Детали тестов */
            .details-section {{
                padding: 40px;
                background: #f8f9fa;
            }}
            
            .section-title {{
                font-size: 2rem;
                margin-bottom: 30px;
                color: var(--dark);
                display: flex;
                align-items: center;
                gap: 15px;
            }}
            
            .section-title i {{
                background: var(--primary);
                color: white;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
            }}
            
            .controls {{
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }}
            
            .filter-btn {{
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                background: white;
                color: var(--dark);
                cursor: pointer;
                font-weight: 600;
                transition: all 0.2s;
                box-shadow: 0 2px 5px var(--shadow);
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .filter-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 8px var(--shadow);
            }}
            
            .filter-btn.active {{
                background: var(--primary);
                color: white;
            }}
            
            .search-box {{
                flex: 1;
                max-width: 400px;
                padding: 10px 20px;
                border: 1px solid var(--border);
                border-radius: 6px;
                font-size: 1rem;
                box-shadow: 0 2px 5px var(--shadow);
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                background: white;
                border-radius: 10px;
                overflow: hidden;
            }}
            
            thead {{
                background: linear-gradient(to right, #2c3e50, #4a6491);
                color: white;
            }}
            
            th {{
                padding: 18px 20px;
                text-align: left;
                font-weight: 600;
                font-size: 1.05rem;
                cursor: pointer;
                transition: background 0.2s;
                position: relative;
            }}
            
            th:hover {{
                background: rgba(0,0,0,0.1);
            }}
            
            th i {{
                margin-left: 8px;
                opacity: 0.7;
                font-size: 0.9rem;
            }}
            
            tr.test-row {{
                border-bottom: 1px solid var(--border);
                transition: background 0.2s;
            }}
            
            tr.test-row:hover {{
                background-color: #f1f8ff;
            }}
            
            .passed-row {{ border-left: 5px solid var(--success); }}
            .failed-row {{ border-left: 5px solid var(--danger); }}
            .skipped-row {{ border-left: 5px solid var(--warning); }}
            
            td {{
                padding: 16px 20px;
                vertical-align: top;
            }}
            
            .status-cell {{
                font-weight: 600;
            }}
            
            .status-badge {{
                display: inline-block;
                padding: 6px 15px;
                border-radius: 20px;
                font-size: 0.95rem;
                text-transform: uppercase;
            }}
            
            .status-badge.passed {{
                background-color: rgba(46, 204, 113, 0.15);
                color: var(--success);
            }}
            
            .status-badge.failed {{
                background-color: rgba(231, 76, 60, 0.15);
                color: var(--danger);
            }}
            
            .status-badge.skipped {{
                background-color: rgba(243, 156, 18, 0.15);
                color: var(--warning);
            }}
            
            .status-icon {{
                margin-right: 8px;
                font-weight: bold;
            }}
            
            .duration-cell {{
                font-weight: 500;
                color: var(--gray);
            }}
            
            .details-cell {{
                max-width: 600px;
            }}
            
            .error-details, .skip-details {{
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                font-family: 'Consolas', monospace;
                white-space: pre-wrap;
                font-size: 0.95rem;
                line-height: 1.5;
            }}
            
            .error-details {{
                background-color: rgba(231, 76, 60, 0.08);
                border-left: 4px solid var(--danger);
                color: #c00;
            }}
            
            .skip-details {{
                background-color: rgba(243, 156, 18, 0.08);
                border-left: 4px solid var(--warning);
                color: #e65100;
            }}
            
            .screenshot-container {{
                margin-top: 15px;
            }}
            
            .screenshot-link {{
                display: flex;
                align-items: center;
                gap: 10px;
                color: var(--primary);
                text-decoration: none;
                font-weight: 500;
                transition: color 0.2s;
                margin-top: 10px;
            }}
            
            .screenshot-link:hover {{
                color: var(--primary-dark);
                text-decoration: underline;
            }}
            
            .screenshot-thumb {{
                width: 120px;
                height: 80px;
                object-fit: cover;
                border-radius: 6px;
                border: 1px solid var(--border);
                transition: transform 0.2s;
            }}
            
            .screenshot-link:hover .screenshot-thumb {{
                transform: scale(1.05);
                box-shadow: 0 3px 10px rgba(0,0,0,0.15);
            }}
            
            /* Системная информация */
            .system-info {{
                padding: 30px 40px;
                background: white;
                border-top: 1px solid var(--border);
            }}
            
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}
            
            .info-card {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }}
            
            .info-card h3 {{
                font-size: 1.2rem;
                color: var(--primary);
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid var(--border);
            }}
            
            .info-item {{
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px dashed var(--border);
            }}
            
            .info-item:last-child {{
                border-bottom: none;
            }}
            
            .info-label {{
                font-weight: 500;
                color: var(--gray);
            }}
            
            .info-value {{
                font-weight: 600;
            }}
            
            /* Футер */
            footer {{
                text-align: center;
                padding: 30px;
                color: var(--gray);
                font-size: 0.95rem;
                background: linear-gradient(to right, #2c3e50, #1a2530);
                color: rgba(255,255,255,0.8);
            }}
            
            .footer-content {{
                max-width: 800px;
                margin: 0 auto;
            }}
            
            .footer-links {{
                display: flex;
                justify-content: center;
                gap: 25px;
                margin: 20px 0;
                flex-wrap: wrap;
            }}
            
            .footer-link {{
                color: rgba(255,255,255,0.8);
                text-decoration: none;
                transition: color 0.2s;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .footer-link:hover {{
                color: white;
            }}
            
            /* Адаптивность */
            @media (max-width: 992px) {{
                .stats-cards {{
                    flex-direction: column;
                    align-items: center;
                }}
                
                .stat-card {{
                    max-width: 100%;
                    width: 100%;
                }}
                
                .summary-stats {{
                    flex-direction: column;
                    gap: 20px;
                }}
            }}
            
            @media (max-width: 768px) {{
                .section-title {{
                    font-size: 1.6rem;
                }}
                
                .controls {{
                    flex-direction: column;
                }}
                
                .search-box {{
                    max-width: 100%;
                }}
                
                th, td {{
                    padding: 12px 15px;
                }}
                
                header {{
                    padding: 30px 20px;
                }}
                
                h1 {{
                    font-size: 2.2rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="header-content">
                    <h1>Отчет о тестировании</h1>
                    <p class="subtitle">Playwright + Pytest</p>
                    
                    <div class="report-meta">
                        <div class="meta-item">
                            <i class="fas fa-calendar"></i>
                            <span>{report_data['timestamp']}</span>
                        </div>
                        <div class="meta-item">
                            <i class="fas fa-clock"></i>
                            <span>{report_data['total_duration']:.2f} сек</span>
                        </div>
                        <div class="meta-item">
                            <i class="fas fa-server"></i>
                            <span>{report_data['env']}</span>
                        </div>
                    </div>
                </div>
            </header>
            
            <div class="summary-stats">
                <div class="summary-item">
                    <h3>Пройдено тестов</h3>
                    <div class="value passed">{passed}</div>
                    <div class="value-sub">{passed_percent}% успешных</div>
                </div>
                <div class="summary-item">
                    <h3>Провалено тестов</h3>
                    <div class="value failed">{failed}</div>
                    <div class="value-sub">{failed_percent}% от общего числа</div>
                </div>
                <div class="summary-item">
                    <h3>Пропущено тестов</h3>
                    <div class="value skipped">{skipped}</div>
                    <div class="value-sub">{skipped_percent}% от общего числа</div>
                </div>
                <div class="summary-item">
                    <h3>Общее время</h3>
                    <div class="value duration">{report_data['total_duration']:.2f} сек</div>
                    <div class="value-sub">Среднее: {(report_data['total_duration']/total if total > 0 else 0):.2f} сек/тест</div>
                </div>
            </div>
            
            <section class="progress-section">
                <div class="progress-header">
                    <div class="progress-title">Общий прогресс выполнения</div>
                    <div class="progress-percent">{passed_percent}%</div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar"></div>
                </div>
                <div class="progress-labels">
                    <div>0%</div>
                    <div>50%</div>
                    <div>100%</div>
                </div>
            </section>
            
            <section class="stats-section">
                <h2 class="stats-title">Статистика тестирования</h2>
                <div class="stats-cards">
                    <div class="stat-card total">
                        <h3>{total}</h3>
                        <p>Всего тестов</p>
                    </div>
                    <div class="stat-card passed">
                        <h3>{passed}</h3>
                        <p>Пройдено</p>
                    </div>
                    <div class="stat-card failed">
                        <h3>{failed}</h3>
                        <p>Провалено</p>
                    </div>
                    <div class="stat-card skipped">
                        <h3>{skipped}</h3>
                        <p>Пропущено</p>
                    </div>
                </div>
            </section>
            
            <section class="details-section">
                <h2 class="section-title">
                    <i class="fas fa-list"></i>
                    Детали выполнения тестов
                </h2>
                
                <div class="controls">
                    <button class="filter-btn active" data-filter="all">
                        <i class="fas fa-layer-group"></i> Все тесты ({total})
                    </button>
                    <button class="filter-btn" data-filter="passed">
                        <i class="fas fa-check-circle"></i> Пройдено ({passed})
                    </button>
                    <button class="filter-btn" data-filter="failed">
                        <i class="fas fa-times-circle"></i> Провалено ({failed})
                    </button>
                    <button class="filter-btn" data-filter="skipped">
                        <i class="fas fa-forward"></i> Пропущено ({skipped})
                    </button>
                    <input type="text" class="search-box" placeholder="Поиск тестов...">
                </div>
                
                <table id="tests-table">
                    <thead>
                        <tr>
                            <th data-sort="number"># <i class="fas fa-sort"></i></th>
                            <th data-sort="name">Название теста <i class="fas fa-sort"></i></th>
                            <th data-sort="status">Статус <i class="fas fa-sort"></i></th>
                            <th data-sort="duration">Длительность <i class="fas fa-sort"></i></th>
                            <th>Детали</th>
                        </tr>
                    </thead>
                    <tbody>
                        {test_rows_html}
                    </tbody>
                </table>
            </section>
            
            <section class="system-info">
                <h2 class="section-title">
                    <i class="fas fa-server"></i>
                    Системная информация
                </h2>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3><i class="fas fa-desktop"></i> Аппаратная платформа</h3>
                        <div class="info-item">
                            <span class="info-label">Платформа:</span>
                            <span class="info-value">{report_data['system']['platform']}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Процессор:</span>
                            <span class="info-value">{report_data['system']['processor']}</span>
                        </div>
                    </div>
                    
                    <div class="info-card">
                        <h3><i class="fas fa-code"></i> Программное обеспечение</h3>
                        <div class="info-item">
                            <span class="info-label">Версия Python:</span>
                            <span class="info-value">{report_data['system']['python_version']}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Окружение:</span>
                            <span class="info-value">{report_data['env']}</span>
                        </div>
                    </div>
                    
                    <div class="info-card">
                        <h3><i class="fas fa-clock"></i> Временные метки</h3>
                        <div class="info-item">
                            <span class="info-label">Начало тестирования:</span>
                            <span class="info-value">{report_data['timestamp']}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Общее время:</span>
                            <span class="info-value">{report_data['total_duration']:.2f} сек</span>
                        </div>
                    </div>
                </div>
            </section>
            
            <footer>
                <div class="footer-content">
                    <p>Отчет сгенерирован автоматически с помощью Playwright и Pytest</p>
                    
                    <div class="footer-links">
                        <a href="#" class="footer-link">
                            <i class="fab fa-github"></i> Исходный код
                        </a>
                        <a href="#" class="footer-link">
                            <i class="fas fa-book"></i> Документация
                        </a>
                        <a href="#" class="footer-link">
                            <i class="fas fa-bug"></i> Сообщить об ошибке
                        </a>
                    </div>
                    
                    <p>Время генерации отчета: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </footer>
        </div>
        
        <script>
            // Функция для сортировки таблицы
            function sortTable(columnIndex, sortType) {{
                const table = document.getElementById('tests-table');
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                const isAscending = table.getAttribute('data-sort-asc') === 'true';
                
                rows.sort((a, b) => {{
                    const aValue = a.cells[columnIndex].textContent.trim();
                    const bValue = b.cells[columnIndex].textContent.trim();
                    
                    if (sortType === 'number') {{
                        return isAscending 
                            ? parseInt(aValue) - parseInt(bValue)
                            : parseInt(bValue) - parseInt(aValue);
                    }}
                    else if (sortType === 'duration') {{
                        const aNum = parseFloat(aValue.replace(' сек', ''));
                        const bNum = parseFloat(bValue.replace(' сек', ''));
                        return isAscending ? aNum - bNum : bNum - aNum;
                    }}
                    else if (sortType === 'status') {{
                        return isAscending 
                            ? aValue.localeCompare(bValue) 
                            : bValue.localeCompare(aValue);
                    }}
                    else {{
                        return isAscending 
                            ? aValue.localeCompare(bValue) 
                            : bValue.localeCompare(aValue);
                    }}
                }});
                
                // Удаляем старые строки
                while (tbody.firstChild) {{
                    tbody.removeChild(tbody.firstChild);
                }}
                
                // Добавляем отсортированные строки
                rows.forEach(row => tbody.appendChild(row));
                
                // Обновляем направление сортировки
                table.setAttribute('data-sort-asc', !isAscending);
            }}
            
            // Добавляем обработчики событий для сортировки
            document.querySelectorAll('th[data-sort]').forEach(header => {{
                header.addEventListener('click', () => {{
                    const sortType = header.getAttribute('data-sort');
                    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
                    sortTable(columnIndex, sortType);
                }});
            }});
            
            // Фильтрация тестов
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    // Убираем активность со всех кнопок
                    document.querySelectorAll('.filter-btn').forEach(b => {{
                        b.classList.remove('active');
                    }});
                    
                    // Делаем текущую кнопку активной
                    btn.classList.add('active');
                    
                    const filter = btn.getAttribute('data-filter');
                    const rows = document.querySelectorAll('#tests-table tbody tr');
                    
                    rows.forEach(row => {{
                        if (filter === 'all') {{
                            row.style.display = '';
                        }} else {{
                            row.style.display = row.classList.contains(filter + '-row') ? '' : 'none';
                        }}
                    }});
                }});
            }});
            
            // Поиск по таблице
            document.querySelector('.search-box').addEventListener('input', (e) => {{
                const searchTerm = e.target.value.toLowerCase();
                const rows = document.querySelectorAll('#tests-table tbody tr');
                
                rows.forEach(row => {{
                    const testName = row.cells[1].textContent.toLowerCase();
                    row.style.display = testName.includes(searchTerm) ? '' : 'none';
                }});
            }});
        </script>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)