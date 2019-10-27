import logging
import urllib.request

from config import TgConfig


def send_msg(msg):
    req = f'https://api.telegram.org/bot{TgConfig.TOKEN}/sendMessage?' \
          f'chat_id={TgConfig.SENDTO}&parse_mode=Markdown&text=+{msg}'
    with urllib.request.urlopen(req) as resp:
        logging.debug(resp.response_read())
