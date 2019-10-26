import lxml.html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
status_list = ["down", "shit", "corrupt", "mumble", "up"]
chrome_options.add_argument('--headless')


class Service:
    def __init__(self, status="up", fdef=0, fatt=0):
        self.status = status
        self.fdef = fdef
        self.fatt = fatt

    def parse(self, el):
        status_el = None
        for status in status_list:
            status_el = el.xpath(f"./div[@class='service-status {status}']")
            if len(status_el) != 0:
                self.status = status
                break
        flags = status_el[0].xpath("./div[@class='service-att-def']")[0].text.split('/')
        self.fdef = int(flags[0])
        self.fatt = int(flags[1])


class Team:
    def __init__(self, name="", services=None):
        if services is None:
            services = []
        self.name = name
        self.services = services

    def parse(self, el):
        n = el.xpath("./div[@class='team']/div[@class='team-name']")
        self.name = n[0].text
        if self.name is None:
            self.name = ""
        services = el.xpath("./div[@class='service']")
        for service in services:
            s = Service()
            s.parse(service)
            self.services.append(s)


class Table:
    def __init__(self, url):
        self.service_names = []
        self.teams = []
        self.url = url

    def parse(self):
        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(self.url)
            time.sleep(3)  # Javascript so fast you can see
            doc = lxml.html.document_fromstring(driver.page_source)
            self.get_services(doc)
            self.get_teams(doc)

    def get_services(self, doc):
        headers = doc.xpath("//div[@class='hdrs']/div[@class='service']")
        for header in headers:
            self.service_names.append(header.text)

    def get_teams(self, doc):
        teams = doc.xpath("//div[@class='tm']")
        for team in teams:
            t = Team()
            t.parse(team)
            self.teams.append(t)

    def __getitem__(self, team_name):
        """

        :type team_name: string
        :rtype: Team, None
        """
        for team in self.teams:
            if team.name == team_name:
                return team
        return None
