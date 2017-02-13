import json
import logging

import requests

import src.application.Domain.Match as Match
import src.application.Domain.Team as Team
import src.util.util as util
from src.application.Crawl.enetscores.CrawlerIncidents import CrawlerIncidents
from src.application.Crawl.enetscores.CrawlerLineup import CrawlerLineup
from src.application.Crawl.enetscores.CrawlerTeam import CrawlerTeam

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

        # check team
        check_team(homefk)
        check_team(awayfk)

        # formations
        if not self.match or not self.match.are_teams_linedup():
            lc = CrawlerLineup(self.match, match_attributes, self.event)
            lc.get_lineups()


        # event incidents
        if not self.match or self.match and not self.match.are_incidents_managed():
            li = CrawlerIncidents(self.match, match_attributes, self.event)
            li.get_incidents()

        if not self.match:
            Match.write_new_match(match_attributes)
        else:
            # update match
            Match.update_match(self.match, match_attributes)


def check_team(team_api_id):
    home_team = Team.read_by_team_api_id(team_api_id)
    if not home_team:
        cm = CrawlerTeam(team_api_id)
        cm.get_team_name()


