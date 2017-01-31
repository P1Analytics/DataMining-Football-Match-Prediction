import src.application.Domain.Team as Team
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
        return Team.read_by_team_api_id(self.home_team_api_id)

    def get_away_team(self):
        '''
        Return the away-team of this match
        :return:
        '''
        return Team.read_by_team_api_id(self.away_team_api_id)

def read_all():
    '''
    Read all the matches
    :return:
    '''
    match_list = []
    for p in SQLLite.read_all("Match"):
        match = Match(p["id"])
        for attribute, value in p.items():
            match.__setattr__(attribute, value)
        match_list.append(match)
    return match_list

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
    match_list = []
    filter = {"home_team_api_id":team_api_id}
    if season:
        filter["season"]=season
    else:
        season = ""

    try:
        return Cache.get_element(str(team_api_id)+"_"+season, "MATCH_HOME")
    except KeyError:
        pass

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