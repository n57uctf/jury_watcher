import logging

import requests

from config import TgConfig
from core.deliver import Deliver


class Telegram(Deliver):
    url = ""
    sendto = ""

    def __init__(self, token=TgConfig.TOKEN, sendto=TgConfig.SENDTO):
        self.url = f'https://api.telegram.org/bot{token}/sendMessage'
        self.sendto = sendto

    def send(self):
        for msg in self.messages:
            logging.debug(f"Message {msg}")
            resp = requests.get(f"{self.url}?chat_id={self.sendto}&parse_mode=Markdown&text={msg}",
                                proxies=TgConfig.PROXY, verify=False)
            logging.debug(resp.text)
