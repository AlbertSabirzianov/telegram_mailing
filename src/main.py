import asyncio
import warnings

from dotenv import load_dotenv
from telegram import Bot

from app.settings import SbSettings, TgSettings
from app.enums import ChatContext
from app.utils import shorten_text_by_paragraphs
from gigachat.chat import get_giga_chat_answer
from yandex import get_picture, get_article
from wiki import get_article_from_wiki


def send_to_channels(channels: list[str], message: str, bot_token: str, picture: bytes) -> None:
    """
    Отправляет сообщение с изображением в указанные Telegram-каналы.

    Параметры:
    channels (list[str]): Список идентификаторов или имен каналов для отправки.
    message (str): Текст сообщения, который будет отправлен в канал.
    bot_token (str): Токен Telegram-бота для аутентификации.
    picture (bytes): Изображение в байтовом формате, которое будет отправлено вместе с сообщением.

    Поведение:
    Для каждого канала из списка пытается отправить фото с подписью.
    В случае ошибки отправки повторяет попытку бесконечно, выводя сообщение об ошибке.
    """
    for ch in channels:
        while True:
            try:
                bot = Bot(token=bot_token)
                asyncio.run(bot.send_photo(chat_id=ch, caption=message.replace("*", ""), photo=picture))
                break
            except:
                print("Can't send to telegram ....")


def main():
    """
    Основная функция программы.

    Логика работы:
    1. Загружает настройки Telegram и Sb из конфигурационных классов.
    2. Запрашивает у пользователя тему поста.
    3. Выполняет поиск статьи в Википедии по теме и добавляет её содержимое в контекст.
    4. Получает текст поста с помощью функции get_giga_chat_answer, используя тему и расширенный контекст.
    5. При необходимости сокращает текст поста до 1000 символов, обрезая по абзацам.
    6. Получает изображение по теме с помощью функции get_picture.
    7. Отправляет сформированный пост с изображением в указанные Telegram-каналы.
    """
    tg_settings = TgSettings()
    sb_settings = SbSettings()

    today_title = input("\n\n Введите тему поста: ")
    print(f"Тема {today_title}")

    article = get_article(today_title)
    if not article:
        warnings.warn("Cant get article from yandex, try from wiki")
        article = get_article_from_wiki(today_title)
        if not article:
            warnings.warn("Cant get article from wiki")
    context = ChatContext.GET_POST_CONTEXT.value + article

    today_post = get_giga_chat_answer(
        message=today_title,
        context=context,
        authorization_sb_code=sb_settings.authorization_sb_code
    )
    print(today_post)

    if len(today_post) > 1000:
        today_post = shorten_text_by_paragraphs(today_post, 1000)
        print("=" * 8)
        print(today_post)

    send_to_channels(
        channels=tg_settings.chanel_names,
        message=today_post,
        bot_token=tg_settings.bot_token,
        picture=get_picture(today_post.split("\n\n")[0])
    )


if __name__ == "__main__":
    load_dotenv()
    main()


