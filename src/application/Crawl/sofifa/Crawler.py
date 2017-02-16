import logging

import requests
from bs4 import BeautifulSoup

import src.application.Domain.League as League
import src.util.util as util
from src.application.Crawl.enetscores.CrawlMatch import CrawlerMatch
from src.application.Crawl.sofifa.CrawlerLeague import CrawlerLeague

log = logging.getLogger(__name__)

class Crawler(object):
    def __init__(self, host_url_league = "http://sofifa.com"
                     , host_url_match  = "http://football-data.mx-api.enetscores.com/page/xhr"):
        self.host_url_league = host_url_league
        self.host_url_match = host_url_match

    def look_for_leagues(self):
        page = requests.get(self.host_url_league+"/leagues").text
        soup = BeautifulSoup(page, "html.parser")
        leagues_found = {}
        table = soup.find('table', {"class": "table table-striped table-hover no-footer"})
        for tr in table.find_all("tr"):
            a = tr.find("a")
            if a:
                league = str(a.string).strip()
                if league.endswith(")"):
                    league = league[:-3].strip()
                link = self.host_url_league + a["href"]
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
                print("ATT: league name not found, a thesarus should be there [ "+league_name+" ]")


    def find_new_league_to_manage(self, leagues_found):
        leagues = League.read_all()
        for league_found in leagues_found:
            new = True
            for league in leagues:
                if league_found in league.name:
                    new = False

            if new:
                print("Found new league:", league_found)


def start_crawling():
    c = Crawler()
    # looking for league
    link_league_found = c.look_for_leagues()
    c.find_thesaurus_legues(link_league_found.values())
    c.find_new_league_to_manage(link_league_found.values())

    for league_link, league_name in link_league_found.items():
        leagues = League.read_by_name(league_name, like=True)
        if len(leagues) == 0:
            log.debug("League by name not found [" + league_name + "]")
        elif len(leagues) == 1:
            league = leagues[0]
            print("Elaborating "+league.name+"...")
            cl = CrawlerLeague(league, league_link)
            cl.start_crawling()
        else:
            log.warning("Too many leagues by name found [" + league_name + "]")

