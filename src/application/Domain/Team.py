from src.application.Domain import Match

import src.util.SQLLite as SQLLite
import src.util.util as util

class Team(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        to_string = "Team "
        attributes = util.read_config_file("src/util/SQLLite.ini","Team")
        for attribute in attributes.keys():
            to_string+=attribute+": "+str(self.__getattribute__(attribute))+", "
        return to_string

    def get_matches(self, season=None):
        return Match.read_matches_by_team(self.team_api_id, season)

def read_all():
    team_list = []
    for p in SQLLite.read_all("Team"):
        team = Team(p["id"])
        for attribute, value in p.items():
            team.__setattr__(attribute, value)
        team_list.append(team)
    return team_list

def read_by_team_api_id(team_api_id):
    sqllite_row = SQLLite.get_connection().select("Team", **{"team_api_id": team_api_id})[0]
    team = Team(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        team.__setattr__(attribute, value)

    return team
