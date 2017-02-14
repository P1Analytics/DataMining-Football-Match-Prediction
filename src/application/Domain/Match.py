import src.util.SQLLite as SQLLite
import src.util.util as util
import src.util.Cache as Cache

import logging

class Match(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        to_string = "Match "
        attributes = util.read_config_file("src/util/SQLLite.ini","Match")
        for attribute in attributes.keys():
            try:
                to_string+=attribute+": "+str(self.__getattribute__(attribute))+", "
            except AttributeError:
                logging.debug("Match :: AttributeError ["+attribute+"]")
        return to_string

    def get_home_team(self):
        '''
        Return the home-team of this match
        :return:
        '''
        import src.application.Domain.Team as Team
        return Team.read_by_team_api_id(self.home_team_api_id)



    def get_away_team(self):
        '''
        Return the away-team of this match
        :return:
        '''
        import src.application.Domain.Team as Team
        return Team.read_by_team_api_id(self.away_team_api_id)

    def get_shots(self, on=True):
        '''
        Return the list of shotons of this match
        :return:
        '''
        import src.application.Domain.Shot as Shot
        return Shot.read_match_shot(self, on)

    def are_teams_linedup(self,):
        hp = "home_player_"
        ap = "away_player_"

        for i in range(1, 11):
            hp_i = hp+str(i)
            ap_i = ap+str(i)
            if not self.__getattribute__(hp_i) or not self.__getattribute__(ap_i):
                return False
        return True

    def are_incidents_managed(self):
        if not self.goal or not self.shoton or not self.shotoff or not self.foulcommit or not self.card or not self.cross or not self.corner or not self.possession:
            return False
        return True



def read_all(column_filter='*'):
    '''
    Read all the matches
    :return:
    '''
    match_list = []
    for p in SQLLite.read_all("Match", column_filter=column_filter):
        match = Match(p["id"])
        for attribute, value in p.items():
            match.__setattr__(attribute, value)
        match_list.append(match)
    return match_list


def read_by_match_api_id(match_api_id):
    '''
    return the match by its api id
    :param match_api_id:
    :return:
    '''
    try:
        return Cache.get_element(str(match_api_id), "MATCH_BY_API_ID")
    except KeyError:
        pass

    try:
        sqllite_row = SQLLite.get_connection().select("Match", **{"match_api_id":str(match_api_id)})[0]
    except IndexError:
        return None
    match = Match(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        match.__setattr__(attribute, value)

    Cache.add_element(str(match.match_api_id), match, "MATCH_BY_API_ID")
    return match

def read_matches_by_league(league_id, season=None):
    '''
    return matches played in the league_id, in a specified season if required
    :param league_id:
    :param season:
    :return:
    '''
    match_list = []
    filter = {"league_id": league_id}

    if season:
        filter["season"]=season
    else:
        season = ""

    try:
        return Cache.get_element(str(league_id)+"_"+season, "MATCH_BY_LEAGUE")
    except KeyError:
        pass

    for sqllite_row in SQLLite.get_connection().select("Match", **filter):
        match = Match(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            match.__setattr__(attribute, value)
        match_list.append(match)

    Cache.add_element(str(league_id) + "_" + season, match_list, "MATCH_BY_LEAGUE")
    return match_list

def read_matches_by_team(team_api_id, season=None):
    '''
    Read matches from DB, of the team identified by team_api_id
    :param team_api_id:
    :param season:
    :return:
    '''
    matches_list = list()
    match_list = read_matches_by_home_team(team_api_id, season)
    match_list.extend(read_matches_by_away_team(team_api_id, season))
    return match_list


def read_matches_by_home_team(team_api_id, season=None):
    '''
    Read matches of the team identified by team_api_id, when it plays at HOME
    :param team_api_id:
    :param season:
    :return:
    '''
    filter = {"home_team_api_id":team_api_id}
    if season:
        filter["season"]=season
    else:
        season = ""
    try:
        return Cache.get_element(str(team_api_id)+"_"+season, "MATCH_HOME")
    except KeyError:
        pass

    match_list = []
    for sqllite_row in SQLLite.get_connection().select("Match", **filter):
        match = Match(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            match.__setattr__(attribute, value)
        match_list.append(match)

    Cache.add_element(str(team_api_id) + "_" + season, match_list, "MATCH_HOME")
    return match_list

def read_matches_by_away_team(team_api_id, season=None):
    '''
    Read matches of the team identified by team_api_id, when it plays AWAY
    :param team_api_id:
    :param season:
    :return:
    '''
    match_list = []
    filter = {"away_team_api_id":team_api_id}
    if season:
        filter["season"]=season
    else:
        season=""

    try:
        return Cache.get_element(str(team_api_id)+"_"+season, "MATCH_AWAY")
    except KeyError:
        pass

    for sqllite_row in SQLLite.get_connection().select("Match", **filter):
        match = Match(sqllite_row["id"])
        for attribute, value in sqllite_row.items():
            match.__setattr__(attribute, value)
        match_list.append(match)

    Cache.add_element(str(team_api_id)+"_"+season, match_list,"MATCH_AWAY")
    return match_list


def read_players_api_id_by_team_api_id(team_api_id, season=None):
    '''
    return a list of player_api_id
    if season is set, consider only that list
    :param team_api_id:
    :param season:
    :return:
    '''
    players_api_id = set()
    filter = {}
    if season:
        filter["season"]=season
    else:
        season=""
    try:
        return Cache.get_element(str(team_api_id)+"_"+season, "MATCH_GET_PLAYERS_BY_TEAM_API_ID")
    except KeyError:
        pass

    filter["home_team_api_id"] = team_api_id
    for sqllite_row in SQLLite.get_connection().select("Match", column_filter="home_player_1, home_player_2, "
                                                                              "home_player_3, home_player_4, "
                                                                              "home_player_5, home_player_6, "
                                                                              "home_player_7, home_player_8, "
                                                                              "home_player_9, home_player_10, "
                                                                              "home_player_11", **filter):
        for home_player_i, player_api_id in sqllite_row.items():
            if player_api_id:
                players_api_id.add(player_api_id)

    del(filter["home_team_api_id"])
    filter["away_team_api_id"] = team_api_id
    for sqllite_row in SQLLite.get_connection().select("Match", column_filter="away_player_1, away_player_2, "
                                                                              "away_player_3, away_player_4, "
                                                                              "away_player_5, away_player_6, "
                                                                              "away_player_7, away_player_8, "
                                                                              "away_player_9, away_player_10, "
                                                                              "away_player_11", **filter):
        for away_player_i, player_api_id in sqllite_row.items():
            if player_api_id:
                players_api_id.add(player_api_id)
    Cache.add_element(str(team_api_id)+"_"+season, players_api_id, "MATCH_GET_PLAYERS_BY_TEAM_API_ID")
    return players_api_id


def write_new_match(match_attributes):
    SQLLite.get_connection().insert("Match", match_attributes)


def update_match(match, match_attributes):
    for attribute, value in match_attributes.items():
        match.__setattr__(attribute, value)
    SQLLite.get_connection().update("Match", match)