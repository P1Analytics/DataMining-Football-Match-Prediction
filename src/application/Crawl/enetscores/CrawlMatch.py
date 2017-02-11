import json
import logging
import requests

import src.util.util as util
import src.application.Domain.Team as Team
from src.application.Crawl.enetscores.CrawlerLineup import CrawlerLineup

log = logging.getLogger(__name__)
class CrawlerMatch(object):
    def __init__(self, match, league, event):
        self.match = match
        self.league = league
        self.event = event

        self.match_link = "http://json.mx-api.enetscores.com/live_data/event/"+event+"/0"
        self.json_match = json.loads(requests.get(self.match_link).text)["i"][0]

        log.debug("Match event ["+event+"] got at link ["+self.match_link+"]")

    def parse_json(self, season):
        status_descfk = self.json_match["status_descfk"]
        status_type = self.json_match["status_type"]
        status_desc_short = self.json_match["status_desc_short"]
        status_desc_name = self.json_match["status_desc_name"]

        match_n = self.json_match["n"]
        sportfk = self.json_match["sportfk"]

        countryfk = self.json_match["countryfk"]
        tournamentfk = self.json_match["tournamentfk"]
        tournament_templatefk = self.json_match["tournament_templatefk"]
        tournament_stagefk = self.json_match["tournament_stagefk"]
        round = self.json_match["round"]        # should be our stage
        live = self.json_match["live"]

        eventfk = self.json_match["eventfk"]
        homefk = self.json_match["homefk"]
        awayfk = self.json_match["awayfk"]
        startdate = self.json_match["startdate"]
        winner = self.json_match["winner"]
        winners = self.json_match["winners"]
        scopes_hash = self.json_match["scopes_hash"]
        incidents_hash = self.json_match["incidents_hash"]

        n_home_yellow_card = 0
        n_home_double_yellow_card = 0
        n_home_red_card = 0
        n_away_yellow_card = 0
        n_away_double_yellow_card = 0
        n_away_red_card = 0

        if type(self.json_match["cards"]) == dict:
            try:
                self.json_match["cards"]["1"]
                n_home_yellow_card = util.get_default(self.json_match["cards"]["1"], "14", 0)
                n_home_double_yellow_card = util.get_default(self.json_match["cards"]["1"], "15", 0)
                n_home_red_card = util.get_default(self.json_match["cards"]["1"], "16", 0)
            except KeyError:
                pass

            try:
                self.json_match["cards"]["2"]
                n_away_yellow_card = util.get_default(self.json_match["cards"]["2"], "14", 0)
                n_away_double_yellow_card = util.get_default(self.json_match["cards"]["2"], "15", 0)
                n_away_red_card = util.get_default(self.json_match["cards"]["2"], "16", 0)
            except KeyError:
                pass

        n_home_goal_first_time = util.get_default(self.json_match["results"]["1"]["r"], "5", 0)
        n_home_goal = util.get_default(self.json_match["results"]["1"]["r"], "1", 0)
        n_away_goal_first_time = util.get_default(self.json_match["results"]["2"]["r"], "5", 0)
        n_away_goal = util.get_default(self.json_match["results"]["2"]["r"], "1", 0)

        #print(round, self.json_match["stats"])

        match_attributes = {}
        match_attributes["country_id"] = self.league.country_id
        match_attributes["league_id"] = self.league.id
        match_attributes["season"] = season
        match_attributes["stage"] = round
        match_attributes["date"] = startdate
        match_attributes["match_api_id"] = eventfk
        match_attributes["home_team_api_id"] = homefk
        match_attributes["away_team_api_id"] = awayfk
        match_attributes["home_team_goal"] = n_home_goal
        match_attributes["away_team_goal"] = n_away_goal

        home_team = Team.read_by_team_api_id(homefk)
        if not home_team:
            team_link = "http://football-data.mx-api.enetscores.com/page/mx/team/"+homefk
            print("Home team not found ["+homefk+"]", team_link)

        away_team = Team.read_by_team_api_id(awayfk)
        if not away_team:
            team_link = "http://football-data.mx-api.enetscores.com/page/mx/team/" + awayfk
            print("Home team not found [" + awayfk + "]", team_link)


        if not self.match or not self.match.are_teams_linedup():
            lc = CrawlerLineup(self.match, self.event)
            lc.get_lineups(match_attributes)




def get_season_by_date(date):
    day = int(date.split("-")[2])
    month = int(date.split("-")[1])
    year = int(date.split("-")[0])

    if month > 6 and day > 15:
        return str(year)+"/"+str(year+1)
    else:
        return str(year-1) + "/" + str(year)


