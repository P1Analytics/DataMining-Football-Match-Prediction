import logging

import requests
from bs4 import BeautifulSoup

import src.application.Domain.League as League
import src.application.Domain.Match as Match
import src.util.util as util
from src.application.Crawl.enetscores.CrawlMatch import CrawlerMatch
from src.application.Crawl.enetscores.CrawlerLeague import CrawlerLeague

log = logging.getLogger(__name__)

class Crawler(object):
    def __init__(self, host_url_match  = "http://football-data.mx-api.enetscores.com/page/xhr"):
        self.host_url_match = host_url_match


    def look_for_matches(self, go_back, stop_when, i=0):
        print("Elaborating matches of the date:", util.get_date(i))
        matches_link = self.host_url_match + "/sport_events/1%2F"+util.get_date(i)+"%2Fbasic_h2h%2F0%2F0/"
        log.debug("Looking for matches of date ["+util.get_date(i)+"] at link ["+matches_link+"]")
        page = requests.get(matches_link).text
        soup = BeautifulSoup(page, "html.parser")

        header_list = soup.find_all('div', {'class':'mx-default-header mx-text-align-left mx-flexbox-container '})
        body_list = soup.find_all('div', {'class': 'mx-table mx-soccer mx-matches-table mx-group-by-stage mx-container mx-league mx-livescore-table'})

        for header, body in zip(header_list, body_list):
            # reading the league
            # Notice that the league is identified also with an attribute called "data-stage"
            league_name = str(header.a.string).strip()
            league_data_stage = header.a.attrs['data-stage']

            # check if the this league corresponds to one of those one managed!

            cl = CrawlerLeague(None, league_data_stage)
            if cl.is_a_managed_league() and len(league_name)>3:

                league = League.read_by_name(league_name)
                if league:
                    season = cl.get_season()
                    for div_event in body.find_all('div', {'class':'mx-stage-events'}):

                        # event correspond to "match_api_id"
                        event = str(div_event.attrs["class"][3]).split("-")[2]

                        match = Match.read_by_match_api_id(event)
                        if not match or not match.are_teams_linedup() or not match.are_incidents_managed():
                            log.debug("Need to crawl match ["+event+"]")
                            cm = CrawlerMatch(match, league, event)
                            cm.parse_json(season)
                        else:
                            log.debug("Not need to crawl match [" + event + "]")

                else:
                    log.debug("League by name not found ["+league_name+", "+league_data_stage+"]")

        if go_back and i != stop_when:
            self.look_for_matches(go_back, stop_when, i+1)


def start_crawling(go_back=False, stop_when=1000):
    c = Crawler()

    # looking for matches
    c.look_for_matches(go_back, stop_when)