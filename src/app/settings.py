from pydantic_settings import BaseSettings


class SbSettings(BaseSettings):
    authorization_sb_code: str


class TgSettings(BaseSettings):
    chanel_names: list[str]
    bot_token: str
