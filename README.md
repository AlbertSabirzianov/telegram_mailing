# telegram_mailing
Скрипт который создаёт пост на джазовую тему и отправляет во все телеграмм каналы
# Как запустить
для начала создайте файл .env в папке src проекта со следующими переменными окружения
```
# Код от сбера giga chat
AUTHORIZATION_SB_CODE="example"
# Список каналов для рассылки
CHANEL_NAMES=["@example_1", "@example_2"]
# Токен бота
BOT_TOKEN=1211212:Example
```
установите зависимости
```commandline
pip install -r src/requirements.txt
```
запустите скрипт
```commandline
python main.py
```