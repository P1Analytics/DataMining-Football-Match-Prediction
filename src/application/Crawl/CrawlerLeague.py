import requests
from bs4 import BeautifulSoup

import src.application.Domain.League as League

class CrawlerLeague(object):
    def __init__(self, league, host_url="http://sofifa.com"):
        self.host_url = host_url
        self.league = league

    def look_for_teams(self, link):
        current_teams = self.league.get_teams_current_season()
        teams_found = {}
        if len(current_teams) == 0:
            page = requests.get(link).text
            soup = BeautifulSoup(page, "html.parser")

            table = soup.find('table', {"class": "table table-striped table-hover table-fixed no-footer"})
            for tr in table.find_all("tr"):
                a = tr.find("a")
                if a:
                    team_name = str(a.string).strip()
                    link = self.host_url+a["href"]
                    teams_found[link] = team_name

        return teams_found

    def find_new_team_to_manage(self, teams_found):
        all_teams = self.league.get_teams()
        for name_team_found in teams_found:
            att = True
            for team in all_teams:
                if name_team_found == team.team_long_name:
                    att = False
            if att:
                print("ATT: team name not found in the league [ "+self.league.name+" ], must be inserted in the DB [ "+name_team_found+" ]")
