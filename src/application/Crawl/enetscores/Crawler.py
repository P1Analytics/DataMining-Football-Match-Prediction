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


    def look_for_matches(self, date):
        print("Elaborating matches of the date:", date)
        matches_link = self.host_url_match + "/sport_events/1%2F"+date+"%2Fbasic_h2h%2F0%2F0/"
        log.debug("Looking for matches of date ["+date+"] at link ["+matches_link+"]")
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
                leagues = League.read_by_name(league_name, like=True)
                if len(leagues) == 0:
                    log.debug("League by name not found [" + league_name + ", " + league_data_stage + "]")
                elif len(leagues)==1:
                    league = leagues[0]
                    print("\tLooking for the league [" + league_name + "]")
                    season = cl.get_season()
                    for div_event in body.find_all('div', {'class':'mx-stage-events'}):

                        # event correspond to "match_api_id"
                        event = str(div_event.attrs["class"][3]).split("-")[2]

                        match = Match.read_by_match_api_id(event)
                        if not match or not match.are_teams_linedup() or not match.are_incidents_managed() or not match.get_home_team() or not match.get_away_team():
                            # crawl when at least one of the following happen:
                            #   - match is not in the DB
                            #   - formation of the teams are not in the DB
                            #   - incidents of the match are not in the DB
                            #   - home_team_api_id is not matched to any team in the DB
                            #   - away_team_api_id is not matched to any team in the DB
                            log.debug("Need to crawl match ["+event+"]")
                            cm = CrawlerMatch(match, league, event)
                            cm.parse_json(season)
                        else:
                            log.debug("Not need to crawl match [" + event + "]")
                else:
                    log.warning("Too many leagues by name found [" + league_name + ", " + league_data_stage + "]")


def start_crawling(go_back=False, stop_when=1000):
    c = Crawler()

    # looking for matches
    for i in range(stop_when):
        date = util.get_date(i)
        c.look_for_matches(date)
        if not go_back:
            break