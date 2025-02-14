import json
import uuid

import requests
from cachetools import TTLCache, cached

from .config import Config, SbUrls

config = Config()
urls = SbUrls()


@cached(TTLCache(ttl=config.token_leave_time_in_seconds, maxsize=10))
def __get_token(authorization_sb_code: str) -> str:
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


