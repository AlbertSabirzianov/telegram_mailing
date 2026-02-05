import random
import time

import requests
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

from app.utils import connection_problems_decorator

Y_URL = "https://yandex.ru/images/search?from=tabbar&text=<q_text>"

EXCLUDE_SUBSTRINGS = ["yandex", "dzen"]


class SDriver:
    """
    Контекстный менеджер для инициализации и корректного завершения
    Selenium WebDriver с настройками для скрытия автоматизации.

    Использует ChromeDriver с опциями:
        - headless режим
        - отключение sandbox и shared memory
        - применение stealth-методов для маскировки автоматизации
        - установка пользовательского User-Agent

    Пример использования:
        with SDriver() as driver:
            driver.get("https://example.com")
    """
    def __enter__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Windows",
            webgl_vendor="Google Inc.",
            render="WebKit",
            fix_hairline=True
        )
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


@connection_problems_decorator
def get_picture(q: str) -> bytes:
    """
    Получает изображение по запросу из яндекса.

    Логика работы:
    1. Открывает страницу поиска изображений Яндекса с заданным текстом запроса.
    2. Ожидает загрузки элементов изображений.
    3. Случайным образом выбирает одно из найденных изображений.
    4. Загружает изображение по URL через requests.
    5. Возвращает содержимое изображения в байтах.

    Параметры:
        q (str): Текст запроса для поиска изображения.

    Возвращает:
        bytes: Содержимое изображения в бинарном формате.

    Особенности:
        - Использует Selenium в headless режиме с маскировкой автоматизации.
        - В случае ошибок повторяет попытку загрузки бесконечно благодаря декоратору.
    """
    with SDriver() as driver:
        driver.get(Y_URL.replace("<q_text>", q))
        img_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.ImagesContentImage-Image"))
        )
        img_url = random.choice(img_elements).get_attribute("src")
    response = requests.get(img_url)
    return response.content


@connection_problems_decorator
def get_article(q: str) -> str:
    with SDriver() as driver:
        driver.get(f"https://yandex.ru/search/?text={q}")
        input_el = driver.find_element(By.CSS_SELECTOR, "input")
        driver.execute_script("""
            let el = document.querySelector('.DistributionSplashScreenModalScene');
            if (el) {
                el.style.display = 'none';
            }
        """)
        input_el.click()
        a_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.Link.organic__greenurl"))
        )
        urls = [a.get_attribute("href") for a in a_elements]
        urls = [
            s for s in urls
            if not any(sub in s.lower() for sub in EXCLUDE_SUBSTRINGS)
        ]
    for url in urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except:
            continue
    return ""
