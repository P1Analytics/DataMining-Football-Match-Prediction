import requests
from bs4 import BeautifulSoup

import src.application.Domain.Team as Team
from src.application.Crawl.sofifa.CrawlerTeam import CrawlerTeam


class CrawlerLeague(object):
    def __init__(self, league, league_link, host_url="http://sofifa.com"):
        self.host_url = host_url
        self.league = league
        self.league_link = league_link

    def look_for_teams(self, link, force_parsing=True):
        current_teams = self.league.get_teams_current_season()
        teams_found = {}
        if len(current_teams) == 0 or force_parsing:
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

    def start_crawling(self):
        # looking for teams
        link_teams_found = self.look_for_teams(self.league_link)

        for team_link, team_name in link_teams_found.items():
            team = Team.read_by_name(team_name)
            ct = CrawlerTeam(team, team_link)
            ct.start_crawling()

