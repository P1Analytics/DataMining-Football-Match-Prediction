import src.util.SQLLite as SQLLite
import src.util.Cache as Cache

class Player(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "Player <id: "+str(self.id)+", player_api_id:"+str(self.player_api_id)+", player_name:"+str(self.player_name)\
               +", player_fifa_api_id:"+str(self.player_fifa_api_id)+", birthday:"+str(self.birthday)\
               +", height:"+str(self.height)+", weight:"+str(self.weight)+">";

def read_all():
    players = []
    for p in SQLLite.read_all("Player"):
        player = Player(p["id"])
        for attribute, value in p.items():
            player.__setattr__(attribute, value)
        players.append(player)
    return players

def read_by_api_id(player_api_id):
    '''
    Read a player by its team_api_id
    :param player_api_id:
    :return:
    '''

    try:
        return Cache.get_element(player_api_id, "PLAYER_BY_API_ID")
    except KeyError:
        pass

    filter = {"player_api_id": player_api_id}
    sqllite_row = SQLLite.get_connection().select("Player", **filter)[0]
    player = Player(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        player.__setattr__(attribute, value)

    Cache.add_element(player_api_id, player, "PLAYER_BY_API_ID")
    return player


