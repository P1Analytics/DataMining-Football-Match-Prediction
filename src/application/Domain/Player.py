import logging

import src.util.SQLLite as SQLLite
import src.util.Cache as Cache
import src.util.util as util

import src.application.Domain.Match as Match
import src.application.Domain.Player_Attributes as Player_Attributes

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


class Player(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "Player <id: "+str(self.id)+", player_api_id:"+str(self.player_api_id)+", player_name:"+str(self.player_name)\
               + ", player_fifa_api_id:"+str(self.player_fifa_api_id)+", birthday:"+str(self.birthday)\
               + ", height:"+str(self.height)+", weight:"+str(self.weight)+">";

    def get_last_player_attributes(self):
        max_date = "0000-00-00"
        last_player_attributes = None

        for player_attributes in self.get_player_attributes():
            if player_attributes.date > max_date:
                max_date = player_attributes.date
                last_player_attributes = player_attributes

        return last_player_attributes

    def get_player_attributes(self):
        return Player_Attributes.read_by_player_fifa_api_id(self.player_fifa_api_id)

    def get_matches(self, season=None, ordered=True, stage = None):
        if util.is_None(self.player_api_id):
            return []
        matches = Match.read_by_player_api_id(self.player_api_id)
        if season:
            matches = [m for m in matches if m.season == season]
        if stage:
            matches = [m for m in matches if m.stage < stage]
        if ordered:
            matches = sorted(matches, key=lambda match: match.stage)
        return matches

    def get_current_team(self):
        try:
            return Cache.get_element(self.id, "PLAYER_CURRENT_TEAM")
        except KeyError:
            pass

        import src.application.Domain.Team as Team
        matches = self.get_matches()
        current_team = None
        if len(matches) > 0:
            last_match = sorted(matches, key=lambda match: match.date)[-1]

            home_player_i = 'home_player_'
            away_player_i = 'away_player_'
            for i in range(11):
                if last_match.__getattribute__(home_player_i+str(i+1)) == self.player_api_id:
                    current_team = Team.read_by_team_api_id(last_match.home_team_api_id)
                    break
                if last_match.__getattribute__(away_player_i+str(i+1)) == self.player_api_id:
                    current_team = Team.read_by_team_api_id(last_match.away_team_api_id)
                    break
        Cache.add_element(self.id, current_team, "PLAYER_CURRENT_TEAM")
        return current_team

    def get_goal_done(self, season=None, stage=None):
        cnt = 0

        matches = self.get_matches(season=season, ordered=True)

        for m in matches:
            if not util.is_None(stage) and m.stage >= stage:
                return cnt
            soup = BeautifulSoup(m.goal, "html.parser")
            for player1 in soup.find_all('player1'):
                if int(str(player1.string).strip()) == self.player_api_id:
                    cnt += 1

        return cnt

    def get_goal_received(self, season=None, stage=None):
        cnt = 0
        current_team = self.get_current_team()
        matches = self.get_matches(season=season, ordered=True)
        for m in matches:
            if not util.is_None(stage) and m.stage >= stage:
                return cnt
            if m.home_team_api_id == current_team.team_api_id:
                cnt += m.away_team_goal
            else:
                cnt += m.home_team_goal

        return cnt

    def get_assist_done(self, season=None, stage=None):
        cnt = 0
        for m in self.get_matches(season=season, ordered=True):
            if not util.is_None(stage) and m.stage >= stage:
                return cnt
            soup = BeautifulSoup(m.goal, "html.parser")
            for player1 in soup.find_all('player2'):
                if int(str(player1.string).strip()) == self.player_api_id:
                    cnt += 1
        return cnt

    def get_presence(self, season=None):
        matches = self.get_matches(season=season, ordered=True)

    def is_gk(self):
        player_attributes = self.get_last_player_attributes()
        if player_attributes:
            overall_gk_attributes = player_attributes.gk_diving
            overall_gk_attributes += player_attributes.gk_handling
            overall_gk_attributes += player_attributes.gk_kicking
            overall_gk_attributes += player_attributes.gk_positioning
            overall_gk_attributes += player_attributes.gk_reflexes

            return overall_gk_attributes / 5 > 50
        else:
            return False

    def save_player_attributes(self, player_attributes):
        Player_Attributes.write_player_attributes(self, player_attributes)

    def set_api_id(self, player_api_id, persist=True):
        self.player_api_id = player_api_id
        if persist:
            update(self)


def read_all():
    players = []
    for p in SQLLite.read_all("Player"):
        player = Player(p["id"])
        for attribute, value in p.items():
            player.__setattr__(attribute, value)
        players.append(player)
    return players


def read_by_api_id(player_api_id):
    """
    Read a player by its api_id
    :param player_api_id:
    :return:
    """
    if util.is_None(player_api_id):
        return None
    try:
        return Cache.get_element(player_api_id, "PLAYER_BY_API_ID")
    except KeyError:
        pass

    filter = {"player_api_id": player_api_id}
    try:
        sqllite_row = SQLLite.get_connection().select("Player", **filter)[0]
    except IndexError:
        return None
    player = Player(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        player.__setattr__(attribute, value)

    Cache.add_element(player.player_fifa_api_id, player, "PLAYER_BY_FIFA_API_ID")
    Cache.add_element(player.player_api_id, player, "PLAYER_BY_API_ID")
    Cache.add_element(player.player_name, player, "PLAYER_BY_NAME")
    return player


def read_by_fifa_api_id(player_fifa_api_id):
    """
    Read a player by its team_fifa_api_id
    :param player_fifa_api_id:
    :return:
    """
    try:
        return Cache.get_element(player_fifa_api_id, "PLAYER_BY_FIFA_API_ID")
    except KeyError:
        pass

    filter = {"player_fifa_api_id": player_fifa_api_id}
    try:
        sqllite_row = SQLLite.get_connection().select("Player", **filter)[0]
    except IndexError:
        return None

    player = Player(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        player.__setattr__(attribute, value)

    Cache.add_element(player.player_fifa_api_id, player, "PLAYER_BY_FIFA_API_ID")
    Cache.add_element(player.player_api_id, player, "PLAYER_BY_API_ID")
    Cache.add_element(player.player_name, player, "PLAYER_BY_NAME")
    return player


def read_by_name(player_name, like=False):
    """
    Read a player by its name
    :param player_name:
    :param like:
    :return:
    """
    filter = {"player_name": player_name}

    if like:
        sqlrows = SQLLite.get_connection().select_like("Player", **filter)
    else:
        sqlrows = SQLLite.get_connection().select("Player", **filter)

    players = []
    for p in sqlrows:
        player = Player(p["id"])
        for attribute, value in p.items():
            player.__setattr__(attribute, value)
        players.append(player)

    return players


def read_by_team_api_id(team_api_id, season=None):
    """
    Return list of players that play in the team identified my team_api_id
    if season is set, consider only that season
    :param team_api_id:
    :param season:
    :return:
    """

    if not season:
        season = ""
    try:
        return Cache.get_element(str(team_api_id)+"_"+season, "PLAYER_BY_TEAM_API_ID")
    except KeyError:
        pass
    players = []
    players_api_id = Match.read_players_api_id_by_team_api_id(team_api_id, season)
    for player_api_id in players_api_id:
        try:
            player = Cache.get_element(player_api_id, "PLAYER_BY_API_ID")
        except KeyError:
            filter = {"player_api_id": player_api_id}
            try:
                sqllite_row = SQLLite.get_connection().select("Player", **filter)[0]
            except IndexError:
                log.warning("Player api id not found in DB ["+str(player_api_id)+"]")
                continue
            player = Player(sqllite_row["id"])
            for attribute, value in sqllite_row.items():
                player.__setattr__(attribute, value)
            Cache.add_element(player_api_id, player, "PLAYER_BY_API_ID")
        players.append(player)

    Cache.add_element(str(team_api_id)+"_"+season, players, "PLAYER_BY_TEAM_API_ID")
    return players


def write_new_player(player_name, player_fifa_api_id, birthday, height, weight, player_api_id=None):
    print("Insering new player", player_name, player_api_id, player_fifa_api_id)
    player_diz = { "player_name": player_name,
                   "player_fifa_api_id": player_fifa_api_id,
                   "birthday": birthday,
                   "height": height,
                   "weight": weight,
                   }
    if not util.is_None(player_api_id):
        player_diz["player_api_id"] = player_api_id

    SQLLite.get_connection().insert("Player", player_diz)
    return read_by_fifa_api_id(player_fifa_api_id)


def update(player):
    SQLLite.get_connection().update("Player", player)
