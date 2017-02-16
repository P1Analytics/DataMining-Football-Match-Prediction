import calendar
import logging
import requests

from bs4 import BeautifulSoup
import src.application.Domain.Team as Team

log = logging.getLogger(__name__)


class CrawlerMatch(object):
    def __init__(self, league, home_team, away_team, match_link, host_url = "http://www.odds.football-data.co.uk"):
        self.league = league
        self.home_team = home_team
        self.away_team = away_team

        self.match_odds_link = host_url+match_link+"all-odds"

        page = requests.get(self.match_odds_link).text
        self.soup = BeautifulSoup(page, "html.parser")
        log.debug("Looking for odds of the match at the link [" + self.match_odds_link + "]")

    def start_crawl(self):
        self.check_teams_match()


        for i, td in enumerate(self.soup.find_all('td', {'title':'Bet 365'})):
            if i==0:
                # home win
                print('home win')
            elif i==1:
                print('Draw')
            elif i==2:
                print("away win")

            print(get_italian_odds((str(td.string).strip())))
        exit(-1)

    def check_teams_match(self):
        start_time_match = self.get_start_time_match()
        for m in self.league.get_matches(date=start_time_match):
            print("match date", m.date)
            print("match home",Team.read_by_team_api_id(m.home_team_api_id))
            print("match away",Team.read_by_team_api_id(m.away_team_api_id))
            print("in home team",self.home_team)
            print("in away team",self.away_team)
            if self.home_team and m.home_team_api_id == self.home_team.team_api_id:
                print("FOUND")
            if self.away_team and m.away_team_api_id == self.away_team.team_api_id:
                print("FOUND")


    def get_start_time_match(self):
        print(self.match_odds_link)
        start_time_match =  str(self.soup.find('p', {'class':'raceTimeContainer'}).string).strip()
        day = start_time_match.split(" ")[1]
        month = {v: k for k,v in enumerate(calendar.month_abbr)}[start_time_match.split(" ")[2][:3]]
        year = start_time_match.split(" ")[3]

        return year + "-" + '{0:02d}'.format(month) + "-" + day


def get_italian_odds(odds_str):
    if "/" in odds_str:
        num = odds_str.split("/")[0]
        den = odds_str.split("/")[1]
        return round(1 + float(num)/float(den),2)
    else:
        return float(odds_str)