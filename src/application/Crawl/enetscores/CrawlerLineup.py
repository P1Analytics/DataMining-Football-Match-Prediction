import logging
import requests

from bs4 import BeautifulSoup
import src.application.Domain.Player as Player

log = logging.getLogger(__name__)

class CrawlerLineup(object):
    def __init__(self, match, match_attrbitues, event):
        self.match = match
        self.match_attributes = match_attrbitues
        self.event = event

        self.match_linedup_link = "http://football-data.mx-api.enetscores.com/page/xhr/event_gamecenter/"+event+"%2Fv2_lineup/"
        page = requests.get(self.match_linedup_link).text
        self.soup = BeautifulSoup(page, "html.parser")

        log.debug("Match linedups event [" + event + "] got at link [" + self.match_linedup_link + "]")

    def get_lineups(self, ):
        self.get_formation(home=True)
        self.get_formation(home=False)


    def get_formation(self,home):
        if home:
            div_class = 'mx-visual-lineup-container mx-landscape mx-home-team'
            player_attributes_api_id = "home_player_"
            player_attributes_X = "home_player_X"
            player_attributes_Y = "home_player_Y"
            index_table_player = 0
        else:
            div_class = 'mx-visual-lineup-container mx-landscape mx-float-left mx-home-away'
            player_attributes_api_id = "away_player_"
            player_attributes_X = "away_player_X"
            player_attributes_Y = "away_player_Y"
            index_table_player = 1


        formation_div = self.soup.find('div', {'class': div_class})
        if not formation_div:
            log.debug("formation not available at the event ["+self.event+"]")
            return

        i = 1
        players_index = {}
        for player_div in formation_div.children:
            try:
                y, x = get_coordinates(str(player_div.attrs['class'][3])[7:])
                player_name = str(player_div.find('div', {'class': 'mx-lineup-incident-name'}).string)

                self.match_attributes[player_attributes_X+str(i)] = x
                self.match_attributes[player_attributes_Y + str(i)] = y
                players_index[player_name] = i
                i += 1
            except AttributeError:
                pass

        table_players = self.soup.find_all('table', {'class': 'mx-lineup-table'})[index_table_player]
        for player_td in table_players.find_all('td', {'class':'mx-player-name'}):
            player_api_id = player_td.a.attrs['data-player']
            last_name_player = get_last_name_playerstr((player_td.a.string).strip())
            i = 0
            current_player_name = ''
            for player_name, player_index in players_index.items():
                if last_name_player in player_name:
                    i = player_index
                    current_player_name = player_name
                    break

            if i > 0:
                self.match_attributes[player_attributes_api_id+str(i)] = player_api_id
                check_player(player_api_id, current_player_name, last_name_player)
            else:
                log.debug("Player with lastname ["+last_name_player+"] not found at the event["+self.event+"]")


def check_player(player_api_id, player_name, last_name_player):
    player = Player.read_by_api_id(player_api_id)
    if not player:
        player = Player.read_by_name(player_name)
        if not player:
            # player not found by name
            log.debug("checking the player: player not found "+ player_name+", id"+ player_api_id)
            log.warning("checking the player: player not found "+ player_name+", id"+ player_api_id)
        else:
            # player found by name but not by api id --> update the api id
            print("player found by name ["+player_name+"] --> updating its api id")
            player.set_api_id(player_api_id, persist=True)

def get_last_name_playerstr(player_name):
    if '.' in player_name:
        return player_name[player_name.index('.')+1 :].strip()
    else:
        return player_name.split(" ")[-1].strip()

def get_coordinates(coordinatesa_str):
    if len(coordinatesa_str) == 2:
        return coordinatesa_str[0], coordinatesa_str[1]
    else:
        return coordinatesa_str[0:2], coordinatesa_str[2]


