import argparse
import logging
import time

from config import Config
from delivers.telegram import Telegram
# TODO: dynamic Tables and Delivers import
from tables.sibirctf import SibirCTF

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(name)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, help="Table source", required=True)
    # parser.add_argument("--jury", type=str, help="Jury type", required=True)
    args = parser.parse_args()
    logging.debug(f"Current args:{str(args)}")
    logging.info(f"Checking {args.source} every {Config.ROUND_TIME}")

    # Logic
    t = SibirCTF(args.source)
    telegram = Telegram()
    t.add_subscriber(telegram)
    while True:
        time.sleep(Config.ROUND_TIME)
        t.get_table()
