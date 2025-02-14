import datetime

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    token_leave_time_in_seconds: int = int(datetime.timedelta(minutes=30).total_seconds())


class SbUrls(BaseSettings):
    token_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    completions_url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


