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

        page = requests.get(self.match_league_link, timeout=10).text
        self.soup = BeautifulSoup(page, "html.parser")
        log.debug("Looking for odds of the league [" + self.league.name + "] at the link [" + self.match_league_link + "]")

    def start_crawl(self):
        for td in self.soup.find_all('td', {'class':'firstColumn'}):
            match_link = td.a.attrs['href']
            match_name = str(td.a.string).strip()
            print("\t|\t|\t-",match_name)

            home_team_str = match_name.split(" v ")[0].strip()
            away_team_str = match_name.split(" v ")[1].strip()



            log.debug("Found the match ["+match_name+"]")
            n_try = 1
            while n_try < 6:
                try:
                    cm = CrawlerMatch(self.league, home_team_str, away_team_str, match_link)
                    cm.start_crawl()
                    break
                except requests.exceptions.ReadTimeout:
                    n_try += 1
