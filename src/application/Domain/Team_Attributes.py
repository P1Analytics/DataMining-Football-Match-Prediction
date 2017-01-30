import src.util.SQLLite as SQLLite
import src.util.util as util

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
    team_attributes_list = []
    for p in SQLLite.read_all("Team_Attributes"):
        team_attributes = Team_Attributes(p["id"])
        for attribute, value in p.items():
            team_attributes.__setattr__(attribute, value)
        team_attributes_list.append(team_attributes)
    return team_attributes_list
