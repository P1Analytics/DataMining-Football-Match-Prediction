import logging
import src.util.util as util
import src.util.Cache as Cache
from src.application.Exception.MLException import MLException
from bs4 import BeautifulSoup


class Shot(object):
    def __init__(self):
        pass

    def __str__(self):
        to_string = "Shot "
        attributes = util.read_config_file("src/util/SQLLite.ini", "Shoton")
        for attribute in attributes.keys():
            try:
                to_string += attribute + ": " + str(self.__getattribute__(attribute)) + ", "
            except AttributeError:
                logging.debug("Match :: AttributeError ["+attribute+"]")
        return to_string


def read_match_shot(match, on=True):
    """
    Return the list of shots (either on or off) of the match
    :param match:
    :param on:
    :return:
    """
    if on:
        on_off = "ON"
    else:
        on_off = "OFF"
    try:
        return Cache.get_element(match.match_api_id, "SHOT"+on_off+"_BY_MATCH_API_ID")
    except KeyError:
        pass

    try:
        if on:
            bs = BeautifulSoup(match.shoton, "html.parser")
        else:
            bs = BeautifulSoup(match.shotoff, "html.parser")
    except TypeError:
        raise MLException(2)

    shot_list = []
    for value in bs.contents[0].children:
        shot = Shot()

        for tag in value.children:
            tag_name = tag.name

            # < stats > < blocked > 1 < / blocked > < / stats >
            if tag_name == "stats":
                stats = {}
                for content in tag.contents:
                    stats[content.name] = str(content.string)
                shot.stats = stats

            # < event_incident_typefk > 61 < / event_incident_typefk >
            elif tag_name == "event_incident_typefk":
                shot.event_incident_typefk = str(tag.string)

            # < coordinates > < value > 11 < / value > < value > 9 < / value > < / coordinates >
            elif tag_name == "coordinates":
                x = str(tag.contents[0].string)
                y = str(tag.contents[1].string)
                shot.coordinates = (x, y)

            # < elapsed > 3 < / elapsed >
            elif tag_name == "elapsed":
                shot.elapsed = str(tag.string)

            # < subtype > blocked_shot < / subtype >
            elif tag_name == "subtype":
                shot.subtype = str(tag.string)

            # < player1 > 41540 < / player1 >
            elif tag_name == "player1":
                shot.player1 = str(tag.string)

            # < sortorder > 2 < / sortorder >
            elif tag_name == "sortorder":
                shot.sortorder = str(tag.string)

            # < team > 8534 < / team >
            elif tag_name == "team":
                shot.team = int(tag.string)

            # < n > 23 < / n >
            elif tag_name == "n":
                shot.n = str(tag.string)

            # < type > shoton < / type >
            elif tag_name == "type":
                shot.type = str(tag.string)

            # < id > 4707358 < / id >
            elif tag_name == "id":
                shot.id = str(tag.string)

            elif tag_name == "elapsed_plus":
                shot.elapsed_plus = str(tag.string)

            elif tag_name == "del":
                shot._del = str(tag.string)
            else:
                logging.debug("Shot :: read_team_shoton > tag not managed [ "+tag_name+" ]")

        shot_list.append(shot)
    Cache.add_element(match.match_api_id, shot_list, "SHOT"+on_off+"_BY_MATCH_API_ID")
    return shot_list
