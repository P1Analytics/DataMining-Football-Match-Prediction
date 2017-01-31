from src.application.Domain import Match
from src.application.Domain import Team_Attributes

import src.util.SQLLite as SQLLite
import src.util.util as util
import src.util.Cache as Cache

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
        '''
        Return matches of this team
        :param season:
        :return:
        '''
        return Match.read_matches_by_team(self.team_api_id, season)

    def get_team_attributes(self,):
        return Team_Attributes.read_by_team_api_id(self.team_api_id)

def read_all():
    '''
    Read all the teams
    :return:
    '''
    team_list = []
    for p in SQLLite.read_all("Team"):
        team = Team(p["id"])
        for attribute, value in p.items():
            team.__setattr__(attribute, value)
        team_list.append(team)
    return team_list

def read_by_team_api_id(team_api_id):
    '''
    Read from the DB the team by its team_api_id
    :param team_api_id:
    :return:
    '''

    try:
        return Cache.get_element(team_api_id, "TEAM_BY_API_ID")
    except KeyError:
        pass

    sqllite_row = SQLLite.get_connection().select("Team", **{"team_api_id": team_api_id})[0]
    team = Team(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        team.__setattr__(attribute, value)

    Cache.add_element(team_api_id, team, "TEAM_BY_API_ID")
    return team
