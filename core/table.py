from typing import List, Dict


class Table:
    status_list = ["down", "shit", "corrupt", "mumble", "up"]
    service_names: List[str] = []
    team_names: List[str] = []
    source = None  # Some source
    cells: Dict = {}  # Services per team
    subscribers: List = []

    def __init__(self, src):
        self.source = src
        pass

    def get_table(self):
        pass

    def get_cells(self):
        pass

    def get_service_names(self):
        pass

    def get_team_names(self):
        pass

    def add_subscriber(self, sub):
        sub.old = self
        self.subscribers.append(sub)

    def remove_subscriber(self, sub):
        sub.old = None
        self.subscribers.remove(sub)

    @staticmethod
    def parse_service(service_el):
        pass
