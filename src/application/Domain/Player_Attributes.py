import logging

import src.util.SQLLite as SQLLite
import src.util.util as util
import src.util.Cache as Cache

log = logging.getLogger(__name__)

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


def read_by_player_fifa_api_id(player_fifa_api_id):
    '''

    :param player_fifa_api_id:
    :return:
    '''
    try:
        return Cache.get_element(player_fifa_api_id, "PLAYER_ATTRIBUTES")
    except KeyError:
        pass
    player_attributes_list = []
    for sqllite_row in SQLLite.get_connection().select("Player_Attributes", **{"player_fifa_api_id": player_fifa_api_id}):
        player_attributes = PlayerAttributes(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            player_attributes.__setattr__(attribute, value)
        player_attributes_list.append(player_attributes)

    Cache.add_element(player_fifa_api_id, player_attributes_list, "PLAYER_ATTRIBUTES")
    return player_attributes_list


def write_player_attributes(player, player_attributes, date=util.get_today_date()+" 00:00:00"):
    log.debug("write_player_attributes of player_fifa_api_id = [" + str(player.player_fifa_api_id) + "]")

    player_attributes["player_fifa_api_id"] = player.player_fifa_api_id
    player_attributes["player_api_id"] = player.player_api_id
    player_attributes["date"] = date

    SQLLite.get_connection().insert("Player_Attributes", player_attributes)
    Cache.del_element(player.player_fifa_api_id, "PLAYER_ATTRIBUTES")
