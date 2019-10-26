import argparse
from core.table import Table
import config
import time
from copy import deepcopy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str, help="Jury URL", required=True)
    args = parser.parse_args()
    cur = Table(args.url)
    cur.parse()
    while True:
        old = deepcopy(cur)
        time.sleep(config.ROUND_TIME)
        cur.parse()