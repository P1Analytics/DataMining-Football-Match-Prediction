import requests
from bs4 import BeautifulSoup

import src.application.Domain.League as League


class Crawler(object):
    def __init__(self, host_url = "http://sofifa.com"):
        self.host_url = host_url

    def look_for_leagues(self):
        page = requests.get(self.host_url+"/leagues").text
        soup = BeautifulSoup(page, "html.parser")
        leagues_found = {}
        table = soup.find('table', {"class": "table table-striped table-hover no-footer"})
        for tr in table.find_all("tr"):
            a = tr.find("a")
            if a:
                league = str(a.string).strip()
                if league.endswith(")"):
                    league = league[:-3].strip()
                link = self.host_url + a["href"]
                leagues_found[link] = league

        return leagues_found


    def find_thesaurus_legues(self, leagues_found):
        leagues = League.read_all()
        for league in leagues:
            att = True
            for league_name in league.name.split("|"):
                if league_name.strip() in leagues_found:
                    att = False
            if att:
                print("ATT: league name not found, a thesarus should be there [ "+league+" ]")


    def find_new_league_to_manage(self, leagues_found):
        leagues = League.read_all()
        for league_found in leagues_found:
            new = True
            for league in leagues:
                if league_found in league.name:
                    new = False

            if new:
                print("Found new league:", league_found)
