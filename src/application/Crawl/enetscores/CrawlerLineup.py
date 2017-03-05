import logging
import requests
import src.application.Domain.Player as Player
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


class CrawlerLineup(object):
    def __init__(self, match, match_attrbitues, event):
        self.match = match
        self.match_attributes = match_attrbitues
        self.event = event

        self.match_linedup_link = \
            "http://football-data.mx-api.enetscores.com/page/xhr/event_gamecenter/"+event+"%2Fv2_lineup/"
        page = requests.get(self.match_linedup_link).text
        self.soup = BeautifulSoup(page, "html.parser")

        log.debug("Match linedups event [" + event + "] got at link [" + self.match_linedup_link + "]")

    def get_lineups(self, ):
        """
        get formation for both the home team, and the away team
        :return:
        """
        self.get_formation(home=True)
        self.get_formation(home=False)

    def get_formation(self, home):
        """
        Get the formation of either the home time ot the away team
        :param home: if true: home_team, otherwise: away_team
        :return:
        """

        # initiate variable depending on the team
        if home:
            div_class = 'mx-visual-lineup-container mx-landscape mx-home-team'
            player_attributes_api_id = "home_player_"
            player_attributes_x = "home_player_X"
            player_attributes_y = "home_player_Y"
            index_table_player = 0
        else:
            div_class = 'mx-visual-lineup-container mx-landscape mx-float-left mx-home-away'
            player_attributes_api_id = "away_player_"
            player_attributes_x = "away_player_X"
            player_attributes_y = "away_player_Y"
            index_table_player = 1

        formation_div = self.soup.find('div', {'class': div_class})
        if not formation_div:
            # div container of formations not present
            log.debug("formation not available at the event ["+self.event+"]")
            return

        i = 1
        players_index = dict()      # KEY: player name, VALUE: index of the player in the formation
        for player_div in formation_div.children:
            try:
                y, x = get_coordinates(str(player_div.attrs['class'][3])[7:])
                player_name = str(player_div.find('div', {'class': 'mx-lineup-incident-name'}).string)

                self.match_attributes[player_attributes_x+str(i)] = x
                self.match_attributes[player_attributes_y + str(i)] = y
                players_index[player_name] = i
                i += 1
            except AttributeError:
                pass

        tables_players = self.soup.find_all('table', {'class': 'mx-lineup-table'})
        if not home and len(tables_players) > 4:
            index_table_player = 2

        table_players = tables_players[index_table_player]
        for player_td in table_players.find_all('td', {'class': 'mx-player-name'}):
            # loop needed to get the player_api_id
            player_api_id = player_td.a.attrs['data-player']
            last_name_player = get_last_name_player(player_td.a.string.strip())

            # start checking last_name_player, with the name found previously
            i = 0
            current_player_name = ''
            for player_name, player_index in players_index.items():
                if last_name_player in player_name:
                    i = player_index
                    current_player_name = player_name
                    break

            if i > 0:
                # player found --> check information in the DB
                self.match_attributes[player_attributes_api_id+str(i)] = player_api_id
                check_player(player_api_id, current_player_name)
            else:
                # inconsistency found about this player
                log.warning("Player with lastname ["+last_name_player+"] not found at the event["+self.event +
                            "], link ["+self.match_linedup_link+"]")


def check_player(player_api_id, player_name):
    """
    Check information about this player in the DB
    :param player_api_id:
    :param player_name:
    :return:
    """
    player = Player.read_by_api_id(player_api_id)
    if not player:
        # player not found in the DB, try to read it by name
        players = Player.read_by_name(player_name, like=True)

        if len(players) == 0:
            # no player found --> insert
            Player.write_new_player(player_name, None, None, None, None, player_api_id=player_api_id)

        if len(players) == 1:
            # player found by name but not by api id --> update the api id
            print("player found by name [" + player_name + "] --> updating its api id")
            players[0].set_api_id(player_api_id, persist=True)

        else:
            # player not found by name
            log.warning("player not found by name [" + player_name + "], player_api_id [" + player_api_id
                        + "]. Remove player_fifa_api_id constraint to add it in the DB")


def get_last_name_player(player_name):
    """
    return the last name of a player
    EX: L. Martini --> Martini
    :param player_name:
    :return:
    """
    if '.' in player_name:
        return player_name[player_name.rfind('.')+1:].strip()
    else:
        return player_name.split(" ")[-1].strip()


def get_coordinates(coordinate_as_str):
    """
    return the coordinates of the player x, y
    :param coordinatesa_str:
    :return:
    """
    if len(coordinate_as_str) == 2:
        return coordinate_as_str[0], coordinate_as_str[1]
    else:
        return coordinate_as_str[0:2], coordinate_as_str[2]
