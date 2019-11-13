import unittest
from copy import deepcopy
from os import getcwd

from core import checks
from core.table import Table
from tables.sibirctf import SibirCTF


class SibirCTFTest(unittest.TestCase):
    t = SibirCTF(f"file://{getcwd()}/Scoreboard.html")

    def test_services(self):
        self.assertEqual(['LNKS'],
                         self.t.get_service_names())

    def test_teams(self):
        self.assertEqual(['Tanuki'],
                         self.t.get_team_names())

    def test_dict(self):
        self.assertEqual({'Tanuki': {'LNKS': {'status': 'down', 'fatt': 0, 'fdef': 972}}},
                         self.t.get_cells())


class CheckTest(unittest.TestCase):
    cur = Table(None)
    old = Table(None)

    def setUp(self) -> None:
        self.cur.service_names = ['TEST']
        self.cur.team_names = ['t1', 't2']
        self.cur.cells = {'t1': {'TEST': {'status': 'up', 'fatt': 0, 'fdef': 0}},
                          't2': {'TEST': {'status': 'up', 'fatt': 0, 'fdef': 0}}}
        self.old = deepcopy(self.cur)

    def test_fb(self):
        self.cur.cells['t1']['TEST']['fatt'] = 1
        self.assertEqual([('TEST', 't1')],
                         checks.table_fb(self.old, self.cur))

    def test_tb(self):
        self.cur.cells['t2']['TEST']['fatt'] = 1
        self.assertEqual(['TEST'],
                         checks.team_bloud(self.old, self.cur, 't2'))

    def test_to(self):
        self.old.cells['t2']['TEST']['fdef'] = 5
        self.cur.cells['t2']['TEST']['fdef'] = 4
        self.assertEqual(['TEST'],
                         checks.team_owned(self.old, self.cur, 't2'))

    def test_tc(self):
        self.old.cells['t2']['TEST']['status'] = "up"
        self.cur.cells['t2']['TEST']['status'] = "down"
        self.assertEqual([('TEST', 'down')],
                         checks.team_change_status(self.old, self.cur, 't2'))


if __name__ == '__main__':
    unittest.main()
