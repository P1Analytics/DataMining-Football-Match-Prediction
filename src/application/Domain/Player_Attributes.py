import src.util.SQLLite as SQLLite
import src.util.util as util

class PlayerAttributes(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        to_string = "PlayerAttributes "
        attributes = util.read_config_file("src/util/SQLLite.ini","Player_Attributes")
        for attribute in attributes.keys():
            to_string+=attribute+": "+str(self.__getattribute__(attribute))+", "
        return to_string

def read_all():
    player_attibutes_list = []
    for p in SQLLite.read_all("Player_Attributes"):
        player_attributes = PlayerAttributes(p["id"])
        for attribute, value in p.items():
            player_attributes.__setattr__(attribute, value)
        player_attibutes_list.append(player_attributes)
    return player_attibutes_list
