import src.util.SQLLite as SQLLite
import src.util.util as util
import src.util.Cache as Cache

import logging

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
                logging.debug("Team_Attributes :: AttributeError ["+attribute+"]")
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


def read_by_team_api_id(team_api_id):
    '''

    :param team_api_id:
    :return:
    '''
    try:
        return Cache.get_element(team_api_id, "TEAM_ATTRIBUTES")
    except KeyError:
        pass
    sqllite_row = SQLLite.get_connection().select("Team_Attributes", **{"team_api_id": team_api_id})[0]
    team_attributes = Team_Attributes(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        team_attributes.__setattr__(attribute, value)

    Cache.add_element(team_api_id, team_attributes, "TEAM_ATTRIBUTES")
    return team_attributes
