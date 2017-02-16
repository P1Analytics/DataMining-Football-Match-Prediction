import logging
import requests

from bs4 import BeautifulSoup

import src.application.Domain.Country as Country
from src.application.Crawl.football_data.CrawlerLeague import CrawlerLeague

log = logging.getLogger(__name__)

# data structure used for matching leagues with bet odds web pages
# KEY : leagues name
# VALUE : leagues name on the bet odds
correspondence = {'Belgium Jupiler League|Belgian Jupiler Pro League':'Belgium First Division A',
                    'England Premier League|English Premier League':'England Premier League',
                    'France Ligue 1|French Ligue 1':'Ligue 1 Orange',
                    'Germany 1. Bundesliga|German 1. Bundesliga':'Bundesliga',
                    'Italy Serie A|Italian Serie A':'Serie A TIM',
                    'Netherlands Eredivisie|Holland Eredivisie':'Eredivisie',
                    'Poland Ekstraklasa|Polish T-Mobile Ekstraklasa':'T-Mobile Ekstraklasa',
                    'Portugal Liga ZON Sagres':'Liga NOS',
                    'Scotland Premier League|Scottish Premiership':'Ladbrokes Premiership',
                    'Spain LIGA BBVA|Spanish Primera Division':'Liga de Fútbol Profesional',
                    'Switzerland Super League|Swiss Super League':'Raiffeisen Super League'}

class Crawler(object):
    def __init__(self, country, host_url_odds  = "http://www.odds.football-data.co.uk"):
        self.host_url_odds = host_url_odds
        self.country = country

        self.link_bet_odds_league_to_check = self.host_url_odds+"/football/"+self.country.name

        page = requests.get(self.link_bet_odds_league_to_check).text
        self.soup = BeautifulSoup(page, "html.parser")
        log.debug("Looking for odds of the country ["+self.country.name+"] at the link ["+self.link_bet_odds_league_to_check+"]")

    def look_for_odds(self):
        for league in self.country.get_leagues():
            for country_league_li in self.soup.find_all('li', {'class':'innerList'}):
                bet_odds_league_name = (str(country_league_li.a.string).strip())
                if correspondence[league.name] == bet_odds_league_name:
                    cl = CrawlerLeague(league, country_league_li.li.a.attrs['href'])
                    cl.start_crawl()



def start_crawling():

    for country in Country.read_all():
        c = Crawler(country)
        c.look_for_odds()