import logging
import requests

from bs4 import BeautifulSoup

import src.application.Domain.Team as Team
from src.application.Crawl.football_data.CrawlerMatch import CrawlerMatch

log = logging.getLogger(__name__)

class CrawlerLeague(object):
    def __init__(self, league, match_link, host_url = "http://www.odds.football-data.co.uk"):
        self.league = league
        self.host_url = host_url
        self.match_league_link = host_url + match_link

        page = requests.get(self.match_league_link).text
        self.soup = BeautifulSoup(page, "html.parser")
        log.debug("Looking for odds of the league [" + self.league.name + "] at the link [" + self.match_league_link + "]")

    def start_crawl(self):
        print(self.match_league_link)
        for td in self.soup.find_all('td', {'class':'firstColumn'}):
            match_link = td.a.attrs['href']
            match_name = str(td.a.string).strip()
            home_team_str = match_name.split("v")[0].strip()
            away_team_str = match_name.split("v")[1].strip()

            home_team = check_team(home_team_str)
            away_team = check_team(away_team_str)

            log.debug("Found the match ["+match_name+"]")
            cm = CrawlerMatch(self.league, home_team, away_team, match_link)
            cm.start_crawl()



def check_team(team_name):
    print(team_name)
    teams = Team.read_by_name(team_name, like=True)
    if len(teams)==0:
        log.warning("No team found with the name ["+team_name+"]")
    elif len(teams)==1:
        print(teams[0])
        return teams[0]
    else:
        log.warning("Too many teams found wiht the name ["+team_name+"]")

    return None
