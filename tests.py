import unittest
from core import checks
from core.table import Table, Team, Service
from copy import deepcopy


class CheckTest(unittest.TestCase):
    cur = Table("")
    old = Table("")

    def setUp(self) -> None:
        self.cur.service_names = ['Test']
        s = Service("up", 0, 0)
        self.cur.teams = [Team("t1", [s]), Team("t2", [deepcopy(s)])]
        self.old = deepcopy(self.cur)

    def test_fb(self):
        self.cur.teams[0].services[0].fatt = 1
        self.assertEqual([(self.cur.service_names[0], self.cur.teams[0].name)], checks.table_fb(self.old, self.cur))

    def test_tb(self):
        self.cur.teams[1].services[0].fatt = 1
        self.assertEqual(checks.team_bloud(self.old, self.cur, self.cur.teams[1].name), [(self.cur.service_names[0])])

    def test_to(self):
        self.old.teams[1].services[0].fdef = 5
        self.cur.teams[1].services[0].fdef = 4
        self.assertEqual(checks.team_owned(self.old, self.cur, self.cur.teams[1].name), [(self.cur.service_names[0])])

    def test_tc(self):
        self.old.teams[1].services[0].status = "up"
        self.cur.teams[1].services[0].status = "down"
        self.assertEqual(checks.team_change_status(self.old, self.cur, self.cur.teams[1].name), [(self.cur.service_names[0], self.cur.teams[1].services[0].status)])


if __name__ == '__main__':
    unittest.main()
