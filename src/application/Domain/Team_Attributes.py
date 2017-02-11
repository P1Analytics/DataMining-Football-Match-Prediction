import src.util.SQLLite as SQLLite
import src.util.util as util
import src.util.Cache as Cache

import logging

log = logging.getLogger(__name__)

class Team_Attributes(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        to_string = "Team_Attributes "
        attributes = util.read_config_file("src/util/SQLLite.ini","Team_Attributes")
        for attribute in attributes.keys():
            try:
                to_string+=attribute+": "+str(self.__getattribute__(attribute))+", "
            except AttributeError:
                log.debug("Team_Attributes :: AttributeError ["+attribute+"]")
        return to_string

def read_all():
    '''
    Read all the team_attributes
    :return:
    '''
    team_attributes_list = []
    for p in SQLLite.read_all("Team_Attributes"):
        team_attributes = Team_Attributes(p["id"])
        for attribute, value in p.items():
            team_attributes.__setattr__(attribute, value)
        team_attributes_list.append(team_attributes)
    return team_attributes_list


def read_by_team_fifa_api_id(team_fifa_api_id):
    '''

    :param team_api_id:
    :return:
    '''
    try:
        return Cache.get_element(team_fifa_api_id, "TEAM_ATTRIBUTES")
    except KeyError:
        pass
    team_attributes_list = []
    for sqllite_row in SQLLite.get_connection().select("Team_Attributes", **{"team_fifa_api_id": team_fifa_api_id}):
        team_attributes = Team_Attributes(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            team_attributes.__setattr__(attribute, value)
        team_attributes_list.append(team_attributes)

    Cache.add_element(team_fifa_api_id, team_attributes_list, "TEAM_ATTRIBUTES")
    return team_attributes_list

def write_team_attributes(team, team_attributes, force=False, date=util.get_today_date()+" 00:00:00"):
    log.debug("write_team_attributes of team_fifa_api_id = ["+team.team_fifa_api_id+"]")

    team_attributes["team_fifa_api_id"]=team.team_fifa_api_id
    team_attributes["team_api_id"]=team.team_api_id
    team_attributes["date"]=date

    SQLLite.get_connection().insert("Team_Attributes", team_attributes)
    Cache.del_element(team.team_fifa_api_id, "TEAM_ATTRIBUTES")



