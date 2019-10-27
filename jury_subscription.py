import argparse
import logging
import time
from copy import deepcopy

import core.checks
from config import Config
from core.table import Table
from core.telegram import send_msg

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(name)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str, help="Jury URL", required=True)
    args = parser.parse_args()
    logging.debug(f"Current args:{str(args)}")
    logging.info(f"Checking {args.url} every {Config.ROUND_TIME}")
    cur = Table(args.url)
    cur.update()
    while True:
        old = deepcopy(cur)
        time.sleep(Config.ROUND_TIME)
        logging.info(f"Updating {args.url}")
        cur.update()
        r = core.checks.table_fb(old, cur)
        if r is not None:
            send_msg(f"FB: {r}")
        r = core.checks.team_change_status(old, cur, Config.TEAM)
        if r is not None:
            send_msg(f"Service status changed: {r}")
        r = core.checks.team_bloud(old, cur, Config.TEAM)
        if r is not None:
            send_msg(f"Our FB: {r}")
        r = core.checks.team_owned(old, cur, Config.TEAM)
        if r is not None:
            send_msg(f"Someone owned us: {r}")
