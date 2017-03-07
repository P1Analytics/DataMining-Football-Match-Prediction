import calendar
import logging
import requests
import time

from bs4 import BeautifulSoup

from src.application.Exception.CrawlException import NoDataException
import src.application.Domain.MatchEvent as MatchEvent
from src.application.Crawl.football_data.CrawlerEvent import CrawlerEvent
import src.util.util as util
import src.application.Domain.Team as Team

log = logging.getLogger(__name__)


class CrawlerMatch(object):
    def __init__(self,
                 league,
                 home_team_str,
                 away_team_str,
                 match_link,
                 host_url="http://www.odds.football-data.co.uk"):

        self.league = league

        self.home_team_str = home_team_str
        self.away_team_str = away_team_str

        self.home_team = check_team(home_team_str)
        self.away_team = check_team(away_team_str)

        self.match_odds_link = host_url+match_link+"all-odds"

        self.page = requests.get(self.match_odds_link, timeout=10).text
        self.soup = BeautifulSoup(self.page, "html.parser")
        log.debug("Looking for odds of the match at the link [" + self.match_odds_link + "]")

    def start_crawl(self):
        """
        start crawling the match event to gather bet-odds
        :return:
        """
        try:
            match_id, match_api_id = self.check_teams_match()
        except ValueError:
            print("Error during crawling ["+self.match_odds_link+"]")
            return
        except NoDataException as e:
            if e.get_code() == 1:
                print("\t|\t|\t* impossible to crawl --> check the DB *")
            return

        # read match event (with bet odds)
        match_event = MatchEvent.read_by_match_id(match_id)
        if not match_event:
            # write new match event
            match_event = MatchEvent.write_new_match_event(match_id)

        relate_events_div = self.soup.find('div', {'class': 'relatedEvents'})
        if util.is_None(relate_events_div):
            log.debug("Events not found for the match ["+self.match_odds_link+"]")
            return

        for event in relate_events_div.find_all('td', {'class': 'event'}):
            # Event related to this match (Match result, goal/no goal, under/over ...)
            event_link = event.a.attrs['href']
            event_name = str(event.a.string).strip()
            ce = CrawlerEvent(match_event, event_name, event_link)
            ce.start_crawl()

    def check_teams_match(self):
        """
        check if the teams of this match are in the DB
        :return:
        """
        start_time_match = self.get_start_time_match()
        print("\t|\t|\t["+start_time_match+"]")
        match = None
        matches = self.league.get_matches(season=util.get_current_season(), date=start_time_match, finished=False)
        for m in matches:
            if self.home_team and m.home_team_api_id == self.home_team.team_api_id:
                match = m
            if self.away_team and m.away_team_api_id == self.away_team.team_api_id:
                match = m

        if match:
            match_id, match_api_id = match.id, match.match_api_id
            self.home_team = update_team(self.home_team, match.home_team_api_id, self.home_team_str)
            self.away_team = update_team(self.away_team, match.away_team_api_id, self.away_team_str)

        elif not util.compare_time_to_now(start_time_match, -7):
            # if match related to the event has not been found, its event date is not in one week
            log.warning("Event match not found [" + self.home_team_str+" vs " + self.away_team_str
                        + "], possible not matching of the date!!")
            raise NoDataException(0)

        else:
            # this match cannot be not present!
            log.warning("No match has been found in this event ["+self.home_team_str+" vs "+self.away_team_str+"]")
            raise NoDataException(1)

        return match_id, match_api_id

    def get_start_time_match(self):
        """
        return the starting time of this match event, used for further controls
        :return:
        """
        n_try = 1
        while n_try <= 5:
            try:
                start_time_match = str(self.soup.find('p', {'class': 'raceTimeContainer'}).string).strip()
                break
            except AttributeError:
                # possible to get an error in retrieving the page
                time.sleep(1*n_try)
                self.page = requests.get(self.match_odds_link).text
                self.soup = BeautifulSoup(self.page, "html.parser")
                n_try += 1
        if n_try == 6:
            log.warning("Impossible to retrieve data about the match ["
                        + self.home_team_str + " v " + self.away_team_str + "]")
            print("Impossible to retrieve data about the match ["
                  + self.home_team_str + " v " + self.away_team_str + "]")
            raise ValueError
        try:
            day = int(start_time_match.split(" ")[1])
            month = {v: k for k, v in enumerate(calendar.month_abbr)}[start_time_match.split(" ")[2][:3]]
            year = start_time_match.split(" ")[3]

            return year + "-" + '{0:02d}'.format(month) + "-" + '{0:02d}'.format(day)
        except IndexError:
            # start time not found
            raise ValueError


def update_team(team, team_api_id, team_name):
    """
    Update useful information about a team in the Database, only if needed!
    :param team:
    :param team_api_id:
    :param team_name:
    :return:
    """
    if team:
        # team already present in the DB, just check the name
        if team_name not in team.team_long_name:
            # Found a team with a different name
            team.team_long_name = team.team_long_name + "|" + team_name
            team = Team.update(team)
            print(team_name, team.team_long_name, "Aggiornamento nome team eseguito")

        if util.is_None(team.team_api_id):
            # If a team with this team api di is present --> merge these two teams,
            # otherwise just update the team

            team_by_api_id = Team.read_by_team_api_id(team_api_id)

            if not util.is_None(team_by_api_id):
                # two team that identifies the same team, each of them with useful information --> merge
                team = Team.merge(team, team_by_api_id)

            else:
                # team not present --> just update the existing one
                log.debug(("Updating the team_api_id ["+str(team_api_id)+"] of the team ["+team_name+"]"))
                team.team_api_id = team_api_id
                team = Team.update(team)
    else:
        # team not found by name or too many teams found with that name
        # --> search team by its api id and update the name if needed
        team = Team.read_by_team_api_id(team_api_id)
        if not team:
            # team not found by api id --> insert new team
            team = Team.write_new_team(team_name, None, team_api_id=team_api_id, team_short_name=None)

        else:
            # team found by team api id
            if not team_name in team.team_long_name:
                # team name not present in the DB --> update the name
                team.team_long_name = team.team_long_name+"|"+team_name
                print("Crawler match update team", team)
                team = Team.update(team)

    if not team:
        log.warning("Found team that is not in the DB, with team_api_id ["+str(team_api_id)+"], and name ["+team_name+"]")

    return team


def check_team(team_name):
    """
    Try to read the team by name from the DB
    :param team_name:
    :return: the team if it has been found, None otherwise
    """
    teams = Team.read_by_name(team_name, like=True)
    if len(teams) == 0:
        log.warning("No team found with the name [" + team_name + "]")
    elif len(teams) == 1:
        return teams[0]
    else:
        log.warning("Too many teams found wiht the name [" + team_name + "]")

    return None
