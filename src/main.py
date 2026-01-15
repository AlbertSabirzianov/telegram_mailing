import asyncio

from dotenv import load_dotenv
from telegram import Bot

from app.settings import SbSettings, TgSettings
from app.enums import ChatContext
from gigachat.chat import get_giga_chat_answer
from yandex.pictures import get_picture

def send_to_channels(channels: list[str], message: str, bot_token: str, picture: bytes) -> None:
    for ch in channels:
        while True:
            try:
                bot = Bot(token=bot_token)
                asyncio.run(bot.send_photo(chat_id=ch, caption=message, photo=picture))
                break
            except:
                print("Can't send to telegramm ....")


def main():
    tg_settings = TgSettings()
    sb_settings = SbSettings()

    today_title = input("\n\n Введите тему поста: ")
    while True:
        print(f"Тема {today_title}")
        today_post = get_giga_chat_answer(
            message=today_title,
            context=ChatContext.GET_POST_CONTEXT.value,
            authorization_sb_code=sb_settings.authorization_sb_code
        )
        print(today_post)
        if len(today_post) < 200 or len(today_post) > 1000:
            print("Post too small or too long")
            continue
        try:
            picture = get_picture(today_title)
        except Exception:
            with open("img.png", "rb") as file:
                picture = file.read()
        send_to_channels(
            channels=tg_settings.chanel_names,
            message=today_post,
            bot_token=tg_settings.bot_token,
            picture=picture
        )
        return


if __name__ == "__main__":
    load_dotenv()
    main()


