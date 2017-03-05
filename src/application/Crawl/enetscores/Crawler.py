import logging

import requests
from bs4 import BeautifulSoup

import src.application.Domain.Match as Match
import src.util.util as util
from src.application.Crawl.enetscores.CrawlMatch import CrawlerMatch
from src.application.Crawl.enetscores.CrawlerLeague import CrawlerLeague

log = logging.getLogger(__name__)


class Crawler(object):
    def __init__(self, host_url_match="http://football-data.mx-api.enetscores.com/page/xhr"):
        self.host_url_match = host_url_match

    def look_for_matches(self, date, force_parsing=False):
        print("Elaborating matches of the date:", date)
        matches_link = self.host_url_match + "/sport_events/1%2F"+date+"%2Fbasic_h2h%2F0%2F0/"
        log.debug("Looking for matches of date ["+date+"] at link ["+matches_link+"]")

        try:
            page = requests.get(matches_link).text
        except Exception as e:
            print(e)
        soup = BeautifulSoup(page, "html.parser")

        header_list = soup.find_all('div', {'class': 'mx-default-header mx-text-align-left mx-flexbox-container '})
        body_list = soup.find_all('div',
        {'class': 'mx-table mx-soccer mx-matches-table mx-group-by-stage mx-container mx-league mx-livescore-table'})
        for header, body in zip(header_list, body_list):
            # reading the league
            # Notice that the league is identified also with an attribute called "data-stage"
            league_name = str(header.a.string).strip()
            league_data_stage = header.a.attrs['data-stage']

            # check if the this league corresponds to one of those one managed!
            cl = CrawlerLeague(league_name, league_data_stage)
            if cl.is_in_a_managed_country() and len(league_name) > 3:
                league = cl.get_league()
                if util.is_None(league):
                    log.warning("Impossible to crawl this league [" + league_name + ", " + league_data_stage + "]")
                    continue

                print("\t- Looking for the league [" + league.name + "]")
                season = cl.get_season()
                for div_event in body.find_all('div', {'class': 'mx-stage-events'}):

                    # event correspond to "match_api_id"
                    event = str(div_event.attrs["class"][3]).split("-")[2]

                    match = Match.read_by_match_api_id(event)
                    if force_parsing \
                            or not match \
                            or not match.are_teams_linedup() \
                            or not match.are_incidents_managed() \
                            or not match.get_home_team() \
                            or not match.get_away_team():
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


def start_crawling(go_back=False, stop_when=1000, starting_date_str=None):
    """

    :param go_back: if True, iterate day by day back-words
    :param stop_when: number of day to be crawled
    :param starting_date_str: starting date of the crawling
    :return:
    """
    c = Crawler()

    # looking for matches
    for i in range(stop_when):
        date = util.get_date(days_to_subtract=i, with_hours=False, starting_date_str=starting_date_str)
        c.look_for_matches(date)

        if not go_back:
            break
