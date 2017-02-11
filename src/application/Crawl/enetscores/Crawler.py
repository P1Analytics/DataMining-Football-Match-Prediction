import logging

import requests
from bs4 import BeautifulSoup

import src.application.Domain.League as League
import src.util.util as util
from src.application.Crawl.enetscores.CrawlMatch import CrawlerMatch
from src.application.Crawl.enetscores.CrawlerLeague import CrawlerLeague

log = logging.getLogger(__name__)

class Crawler(object):
    def __init__(self, host_url_match  = "http://football-data.mx-api.enetscores.com/page/xhr"):
        self.host_url_match = host_url_match


    def look_for_matches(self, go_back):
        today_matches_link = self.host_url_match + "/sport_events/1%2"+util.get_today_date()+"%2Fbasic_h2h%2F0%2F0/"
        log.debug("Looking for matches at ["+today_matches_link+"]")
        page = requests.get(today_matches_link).text
        soup = BeautifulSoup(page, "html.parser")

        header_list = soup.find_all('div', {'class':'mx-default-header mx-text-align-left mx-flexbox-container '})
        body_list = soup.find_all('div', {'class': 'mx-table mx-soccer mx-matches-table mx-group-by-stage mx-container mx-league mx-livescore-table'})

        for header, body in zip(header_list, body_list):
            # reading the league
            # Notice that the league is identified also with an attribute called "data-stage"
            league_name = str(header.a.string).strip()
            league_data_stage = header.a.attrs['data-stage']

            # check if the this league corresponds to one of those one managed!
            link_league_to_check = "http://football-data.mx-api.enetscores.com/page/xhr/standings/1%2F0%2F0%2F0%2F"+league_data_stage+"%2F0/"
            cl = CrawlerLeague(None, link_league_to_check)
            if cl.is_a_managed_league(league_data_stage) and len(league_name)>3:

                league = League.read_by_name(league_name)
                if league:
                    print(league_name, league_data_stage)
                    for div_event in body.find_all('div', {'class':'mx-stage-events'}):
                        event = str(div_event.attrs["class"][3]).split("-")[2]
                        event_link = "http://json.mx-api.enetscores.com/live_data/event/"+event+"/0"
                        cm = CrawlerMatch(league, event_link)
                        cm.parse_json()
                else:
                    log.debug("League by name not found ["+league_name+", "+league_data_stage+"]")


def start_crawling(go_back=False):
    c = Crawler()

    # looking for matches
    c.look_for_matches(go_back)