import src.application.Domain.Team as Team
import src.util.SQLLite as SQLLite
import src.util.util as util

import logging

class Match(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        to_string = "Match "
        attributes = util.read_config_file("src/util/SQLLite.ini","Match")
        for attribute in attributes.keys():
            try:
                to_string+=attribute+": "+str(self.__getattribute__(attribute))+", "
            except AttributeError:
                logging.debug("Match :: AttributeError ["+attribute+"]")
        return to_string

    def get_home_team(self):
        return Team.read_by_team_api_id(self.home_team_api_id)

    def get_away_team(self):
        return Team.read_by_team_api_id(self.away_team_api_id)

def read_all():
    match_list = []
    for p in SQLLite.read_all("Match"):
        match = Match(p["id"])
        for attribute, value in p.items():
            match.__setattr__(attribute, value)
        match_list.append(match)
    return match_list

def read_matches_by_league(league_id, season=None):
    match_list = []
    filter = {"league_id": league_id}

    if season:
        filter["season"]=season

    for sqllite_row in SQLLite.get_connection().select("Match", **filter):
        match = Match(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            match.__setattr__(attribute, value)
        match_list.append(match)
    return match_list

def read_matches_by_team(team_api_id, season=None):
    match_list = read_matches_by_home_team(team_api_id, season)
    match_list.extend(read_matches_by_away_team(team_api_id, season))
    return match_list


def read_matches_by_home_team(team_api_id, season=None):
    match_list = []
    filter = {"home_team_api_id":team_api_id}
    if season:
        filter["season"]=season
    for sqllite_row in SQLLite.get_connection().select("Match", **filter):
        match = Match(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            match.__setattr__(attribute, value)
        match_list.append(match)
    return match_list

def read_matches_by_away_team(team_api_id, season=None):
    match_list = []
    filter = {"away_team_api_id":team_api_id}
    if season:
        filter["season"]=season
    for sqllite_row in SQLLite.get_connection().select("Match", **filter):
        match = Match(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            match.__setattr__(attribute, value)
        match_list.append(match)
    return match_list