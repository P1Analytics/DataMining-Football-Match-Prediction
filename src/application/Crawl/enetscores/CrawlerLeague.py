import logging
import requests
from bs4 import BeautifulSoup


import src.application.Domain.Country as Country
import src.application.Domain.League as League
import src.util.Cache as Cache

log = logging.getLogger(__name__)

class CrawlerLeague(object):
    def __init__(self, league_name, league_data_stage):
        self.league_name = league_name
        self.league_data_stage = league_data_stage

        self.link_league_to_check = "http://football-data.mx-api.enetscores.com/page/xhr/standings/1%2F0%2F0%2F0%2F" + self.league_data_stage + "%2F0/"
        log.debug("Check by league data stage [" + self.league_data_stage + "] if this is a managed leage [" + self.link_league_to_check + "]")

    def is_in_a_managed_country(self):
        '''
        check if the league is correct
        "http://football-data.mx-api.enetscores.com/page/xhr/standings/1%2F0%2F0%2F0%2F"+league_data_stage+"%2F0/"
        :return:
        '''
        try:
            return Cache.get_element(self.league_data_stage, "CRAWL_LEAGUE_MANAGED")
        except KeyError:
            pass
        page = requests.get(self.link_league_to_check).text
        self.soup = BeautifulSoup(page, "html.parser")
        country_name = str(self.soup.find('span', {'class':'mx-country-dropdown-name'}).string).strip()
        countries = Country.read_by_name(country_name, like=True)
        if len(countries)==0:
            # this country is not managed!!
            Cache.add_element(self.league_data_stage, False, "CRAWL_LEAGUE_MANAGED")
            return False
        else:
            if len(countries)==1:
                country = countries[0]
                for league in country.get_leagues():
                    if self.league_name in league.name:
                        self.league = league
            Cache.add_element(self.league_data_stage, True, "CRAWL_LEAGUE_MANAGED")
            return True

    def get_league(self):
        return self.league

    def get_season(self):
        '''
        return the season of this league
        :return:
        '''
        try:
            return Cache.get_element(self.league_data_stage, "CRAWL_LEAGUE_SEASON")
        except KeyError:
            pass

        if not self.soup:
            page = requests.get(self.link_league_to_check).text
            self.soup = BeautifulSoup(page, "html.parser")

        div_season = self.soup.find('div', {'class':'mx-dropdown-container mx-flexbox mx-float-left mx-tournament-dropdown'})
        season = str(div_season.span.string)
        Cache.add_element(self.league_data_stage, season, "CRAWL_LEAGUE_SEASON")

        return season
