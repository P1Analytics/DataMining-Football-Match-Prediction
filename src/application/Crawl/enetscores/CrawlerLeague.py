import requests
from bs4 import BeautifulSoup

import src.application.Domain.Country as Country
import src.application.Domain.Team as Team
import src.util.Cache as Cache
from src.application.Crawl.sofifa.CrawlerTeam import CrawlerTeam


class CrawlerLeague(object):
    def __init__(self, league, league_link):
        self.league = league
        self.league_link = league_link

    def is_a_managed_league(self, league_data_stage):
        '''
        check if the league is correct
        "http://football-data.mx-api.enetscores.com/page/xhr/standings/1%2F0%2F0%2F0%2F"+league_data_stage+"%2F0/"
        :return:
        '''

        try:
            return Cache.get_element(league_data_stage, "LEAGUE_MANAGED")
        except KeyError:
            pass

        page = requests.get(self.league_link).text
        soup = BeautifulSoup(page, "html.parser")
        coutnry_name = str(soup.find('span', {'class':'mx-country-dropdown-name'}).string).strip()
        country = Country.read_by_name(coutnry_name)
        if not country:
            # this country is not managed!!
            Cache.add_element(league_data_stage, False, "LEAGUE_MANAGED")
            return False
        else:
            Cache.add_element(league_data_stage, True, "LEAGUE_MANAGED")
            return True

