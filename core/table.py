import time
from typing import List, Dict

import lxml.html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

status_list = ["down", "shit", "corrupt", "mumble", "up"]


class Table:
    def __init__(self, url):
        self.service_names: List[str] = []
        self.team_names: List[str] = []
        self.teams: Dict = {}
        self.url: str = url
        if url is not None:
            self.update()

    def update(self):
        data: str = ""
        if "file://" in self.url:
            with open(self.url[7:], "r") as f:
                data = f.read()
        else:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            with webdriver.Chrome(options=chrome_options) as driver:
                driver.get(self.url)
                time.sleep(3)  # Javascript so fast you can see
                data = driver.page_source
        doc = lxml.html.document_fromstring(data)
        self.get_service_names(doc)
        self.get_team_names(doc)
        self.get_teams(doc)

    def get_service_names(self, doc):
        headers = doc.xpath("//div[@class='hdrs']/div[@class='service']")
        for header in headers:
            self.service_names.append(header.text)

    def get_teams(self, doc):
        teams = doc.xpath("//div[@class='tm']")
        for team in teams:
            name = team.xpath("./div[@class='team']/div[@class='team-name']")[0].text
            self.teams[name] = {}
            # Services
            services = team.xpath("./div[@class='service']")
            if not self.service_names:
                self.get_service_names(doc)
            if not self.team_names:
                self.get_team_names(doc)
            for i, service in enumerate(services):
                self.teams[name][self.service_names[i]] = self.parse_service(service)

    def get_team_names(self, doc):
        teams = doc.xpath("//div[@class='tm']/div[@class='team']/div[@class='team-name']")
        for team in teams:
            self.team_names.append(team.text)

    @staticmethod
    def parse_service(service_el):
        service_template = {"status": None, "fatt": 0, "fdef": 0}
        status_el = None
        for status in status_list:
            status_el = service_el.xpath(f"./div[@class='service-status {status}']")
            if len(status_el) != 0:
                service_template['status'] = status
                break
        flags = status_el[0].xpath("./div[@class='service-att-def']")[0].text.split('/')
        service_template['fdef'] = int(flags[0])
        service_template['fatt'] = int(flags[1])
        return service_template
