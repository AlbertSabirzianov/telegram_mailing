import json
import uuid

import requests
from cachetools import TTLCache, cached

from .config import Config, SbUrls
from app.utils import connection_problems_decorator

config = Config()
urls = SbUrls()


@cached(TTLCache(ttl=config.token_leave_time_in_seconds, maxsize=10))
@connection_problems_decorator
def __get_token(authorization_sb_code: str) -> str:
    """
    Получает и кеширует OAuth токен доступа для GigaChat API.

    Параметры:
        authorization_sb_code (str): Код авторизации в формате Basic для получения токена.

    Возвращает:
        str: Токен доступа (access_token).

    Особенности:
        - Использует POST-запрос с заголовками и payload для получения токена.
        - Кеширует результат с помощью TTLCache на время, заданное в конфигурации (token_leave_time_in_seconds).
        - Максимальный размер кеша — 10 токенов.
        - Генерирует уникальный RqUID для каждого запроса.
    """
    payload ='scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f'Basic {authorization_sb_code}'
    }
    response = requests.request(
        "POST",
        urls.token_url,
        headers=headers,
        data=payload,
        verify=False
    )
    return response.json()["access_token"]


def get_giga_chat_answer(message: str, context: str, authorization_sb_code: str) -> str:
    """
    Отправляет запрос к GigaChat API для получения ответа на заданное сообщение в указанном контексте.

    Параметры:
        message (str): Текст запроса пользователя.
        context (str): Контекст системного сообщения, задающий стиль и цель ответа.
        authorization_sb_code (str): Код авторизации для получения токена доступа.

    Возвращает:
        str: Текст ответа, сгенерированного GigaChat.

    Особенности:
        - Формирует JSON payload с моделью, сообщениями и параметрами.
        - Использует токен доступа, полученный через __get_token, в заголовках.
        - В случае сетевых ошибок повторяет попытку запроса бесконечно с выводом сообщения об ошибке.
    """
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False,
        "update_interval": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {__get_token(authorization_sb_code)}'
    }
    while True:
        try:
            response = requests.request(
                "POST",
                urls.completions_url,
                headers=headers,
                data=payload,
                verify=False
            )
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException:
            print("Can't connect to gigachat.. try again")
            continue


