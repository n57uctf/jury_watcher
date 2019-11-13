from copy import deepcopy

from config import Config
from core.checks import *
from core.table import Table


class Deliver:
    messages = []
    old: Table = None

    def update(self, cur):
        self.checks(cur)
        self.send()
        self.old = deepcopy(cur)

    def checks(self, cur):
        self.messages = []
        result = table_fb(self.old, cur)
        if result:
            self.messages.append(f"First Bloud: {result}")
        result = team_bloud(self.old, cur, Config.TEAM)
        if result:
            self.messages.append(f"Team FB: {result}")
        result = team_owned(self.old, cur, Config.TEAM)
        if result:
            self.messages.append(f"Owned services: {result}")
        result = team_change_status(self.old, cur, Config.TEAM)
        if result:
            self.messages.append(f"Services changed self status: {result}")

    def send(self):
        pass
