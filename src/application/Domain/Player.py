import src.util.SQLLite as SQLLite

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

