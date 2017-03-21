import logging
import requests
import src.application.Domain.League as League
from bs4 import BeautifulSoup
from src.application.Crawl.sofifa.CrawlerLeague import CrawlerLeague

log = logging.getLogger(__name__)


class rCrawler(object):
    def __init__(self, host_url_league="http://sofifa.com"):
        self.host_url_league = host_url_league

    def look_for_leagues(self):
        """
        look for league
        :return:
        """
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


def find_new_league_to_manage(leagues_found):
    """
    Return leagues that are not managed right now, but they can be
    :param leagues_found:
    :return:
    """
    new_league_names = []
    leagues = League.read_all()
    for league_found in leagues_found:
        new = True
        for league in leagues:
            if league_found in league.name:
                new = False
        if new:
            new_league_names.append(league_found)

    return new_league_names


def find_thesaurus_legues(leagues_found):
    """
    try to match leagues in the DB with those one found on the web page
    :param leagues_found:
    :return:
    """
    leagues = League.read_all()
    for league in leagues:
        att = True
        for league_name in league.name.split("|"):
            if league_name.strip() in leagues_found:
                att = False
        if att:
            print("ATT: league name not found, a thesarus should be there [ "+league_name+" ]")


def start_crawling():
    """

    :return:
    """
    c = Crawler()
    link_league_found = c.look_for_leagues()
    find_thesaurus_legues(link_league_found.values())

    for new_league_name in find_new_league_to_manage(link_league_found.values()):
        log.info("New league that can be managed [" + new_league_name + "]")

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
