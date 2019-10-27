import unittest
from copy import deepcopy
from os import getcwd

from core import checks
from core.table import Table


class TableTest(unittest.TestCase):
    t = None

    def setUp(self) -> None:
        self.t = Table(f"file://{getcwd()}/Scoreboard.html")

    def test_services(self):
        self.assertEqual(['LNKS'],
                         self.t.service_names)

    def test_teams(self):
        self.assertEqual(['Tanuki'],
                         self.t.team_names)

    def test_dict(self):
        self.assertEqual({'Tanuki': {'LNKS': {'status': 'down', 'fatt': 0, 'fdef': 972}}},
                         self.t.teams)


class CheckTest(unittest.TestCase):
    cur = Table(None)
    old = Table(None)

    def setUp(self) -> None:
        self.cur.service_names = ['TEST']
        self.cur.team_names = ['t1', 't2']
        self.cur.teams = {'t1': {'TEST': {'status': 'up', 'fatt': 0, 'fdef': 0}},
                          't2': {'TEST': {'status': 'up', 'fatt': 0, 'fdef': 0}}}
        self.old = deepcopy(self.cur)

    def test_fb(self):
        self.cur.teams['t1']['TEST']['fatt'] = 1
        self.assertEqual([('TEST', 't1')],
                         checks.table_fb(self.old, self.cur))

    def test_tb(self):
        self.cur.teams['t2']['TEST']['fatt'] = 1
        self.assertEqual(['TEST'],
                         checks.team_bloud(self.old, self.cur, 't2'))

    def test_to(self):
        self.old.teams['t2']['TEST']['fdef'] = 5
        self.cur.teams['t2']['TEST']['fdef'] = 4
        self.assertEqual(['TEST'],
                         checks.team_owned(self.old, self.cur, 't2'))

    def test_tc(self):
        self.old.teams['t2']['TEST']['status'] = "up"
        self.cur.teams['t2']['TEST']['status'] = "down"
        self.assertEqual([('TEST', 'down')],
                         checks.team_change_status(self.old, self.cur, 't2'))


if __name__ == '__main__':
    unittest.main()
