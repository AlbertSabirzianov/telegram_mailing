from pydantic_settings import BaseSettings


class SbSettings(BaseSettings):
    """
    Настройки для сервиса GigaChat.

    Атрибуты:
        authorization_sb_code (str): Код авторизации для доступа к сервису GigaChat.

    Значения по умолчанию загружаются из переменных окружения или .env файла.
    """
    authorization_sb_code: str


class TgSettings(BaseSettings):
    """
    Настройки для Telegram-бота.

    Атрибуты:
        chanel_names (list[str]): Список имён или идентификаторов Telegram-каналов,
         куда бот будет отправлять сообщения.
        bot_token (str): Токен Telegram-бота для аутентификации и отправки сообщений.

    Значения загружаются из переменных окружения или .env файла.
    """
    chanel_names: list[str]
    bot_token: str
