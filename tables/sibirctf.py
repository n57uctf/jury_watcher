import time

import lxml.html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from core.table import Table


class SibirCTF(Table):
    def __init__(self, src):
        super().__init__(src)
        data: str = ""
        if "file://" in self.source:
            with open(self.source[7:], "r") as f:
                data = f.read()
        else:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            with webdriver.Chrome(options=chrome_options) as driver:
                driver.get(self.source)
                time.sleep(3)  # Javascript so fast you can see
                data = driver.page_source
        self.source = lxml.html.document_fromstring(data)
        self.get_table()

    def get_table(self):
        self.get_service_names()
        self.get_team_names()
        self.get_cells()
        for sub in self.subscribers:
            sub.update(self)

    def get_cells(self):
        teams = self.source.xpath("//div[@class='tm']")
        self.cells = {}
        for team in teams:
            name = team.xpath("./div[@class='team']/div[@class='team-name']")[0].text
            self.cells[name] = {}
            # Services
            services = team.xpath("./div[@class='service']")
            if not self.service_names:
                self.get_service_names()
            if not self.team_names:
                self.get_team_names()
            for i, service in enumerate(services):
                self.cells[name][self.service_names[i]] = self.parse_service(service)
        return self.cells

    def get_service_names(self):
        self.service_names = []
        headers = self.source.xpath("//div[@class='hdrs']/div[@class='service']")
        for header in headers:
            self.service_names.append(header.text)
        return self.service_names

    def get_team_names(self):
        self.team_names = []
        teams = self.source.xpath("//div[@class='tm']/div[@class='team']/div[@class='team-name']")
        for team in teams:
            self.team_names.append(team.text)
        return self.team_names

    @staticmethod
    def parse_service(service_el):
        service_template = {"status": None, "fatt": 0, "fdef": 0}
        status_el = None
        for status in Table.status_list:
            status_el = service_el.xpath(f"./div[@class='service-status {status}']")
            if len(status_el) != 0:
                service_template['status'] = status
                break
        flags = status_el[0].xpath("./div[@class='service-att-def']")[0].text.split('/')
        service_template['fdef'] = int(flags[0])
        service_template['fatt'] = int(flags[1])
        return service_template
