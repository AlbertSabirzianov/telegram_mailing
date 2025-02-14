import asyncio
import random

from dotenv import load_dotenv
from telegram import Bot

from app.settings import SbSettings, TgSettings
from app.enums import ChatMessage, ChatContext
from gigachat.chat import get_giga_chat_answer


def parse_titles(response: str) -> list[str]:
    # Разбиваем текст по строкам
    lines = response.strip().split('\n')
    # Ищем строки, которые начинаются с цифры и точки
    ideas = [line.strip().split('.')[1] for line in lines if line.strip().startswith(tuple(f"{i}." for i in range(1, 11)))]
    return ideas


def get_list_of_titles(authorization_sb_code: str) -> list[str]:
    response: str = get_giga_chat_answer(
        message=ChatMessage.GET_TITLES_QUERY.value,
        context=ChatContext.GET_TITLES_CONTEXT.value,
        authorization_sb_code=authorization_sb_code
    )
    return parse_titles(response)


def send_to_channels(channels: list[str], message: str, bot_token: str) -> None:
    for ch in channels:
        bot = Bot(token=bot_token)
        asyncio.run(bot.send_message(chat_id=ch, text=message))


def main():
    tg_settings = TgSettings()
    sb_settings = SbSettings()

    # print(tg_settings.chanel_names)
    titles = get_list_of_titles(sb_settings.authorization_sb_code)

    today_title = random.choice(titles)
    today_post = get_giga_chat_answer(
        message=today_title,
        context=ChatContext.GET_POST_CONTEXT.value,
        authorization_sb_code=sb_settings.authorization_sb_code
    )
    send_to_channels(
        channels=tg_settings.chanel_names,
        message=today_post,
        bot_token=tg_settings.bot_token
    )


if __name__ == "__main__":
    load_dotenv()
    main()



