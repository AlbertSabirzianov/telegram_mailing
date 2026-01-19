import datetime

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Конфигурация приложения.

    Атрибуты:
        token_leave_time_in_seconds (int): Время жизни токена в секундах.
            По умолчанию установлено в 30 минут (1800 секунд).
            Используется для кеширования токена доступа с ограничением по времени.
    """
    token_leave_time_in_seconds: int = int(datetime.timedelta(minutes=30).total_seconds())


class SbUrls(BaseSettings):
    """
    URL-адреса API для сервиса Sb.

    Атрибуты:
        token_url (str): URL для получения OAuth токена.
        completions_url (str): URL для запроса к API генерации ответов GigaChat.
    """
    token_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    completions_url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


