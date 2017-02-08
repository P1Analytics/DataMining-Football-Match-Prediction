import src.application.Domain.Match as Match
import src.util.util as util
import src.util.Cache as Cache
import src.util.SQLLite as SQLLite

import logging

class League(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        to_string = "League "
        attributes = util.read_config_file("src/util/SQLLite.ini","League")
        for attribute in attributes.keys():
            try:
                to_string+=attribute+": "+str(self.__getattribute__(attribute))+", "
            except AttributeError:
                logging.debug("League :: AttributeError ["+attribute+"]")
        return to_string

    def get_seasons(self):
        '''
        Return the stored seasons of this league
        :return:
        '''
        try:
            return Cache.get_element(self.id, "SEASONS_BY_LEAGUE")
        except KeyError:
            pass
        seasons = []
        query = "SELECT distinct(season) FROM Match WHERE league_id='"+str(self.id)+"'"
        for sqllite_row in SQLLite.get_connection().execute_query(query):
            seasons.append(sqllite_row[0])

        Cache.add_element(self.id, seasons, "SEASONS_BY_LEAGUE")
        return seasons

    def get_matches(self,season=None):
        return Match.read_matches_by_league(self.id, season)

    def get_teams(self, season=None):
        '''
        Retrun teams of a league, can be filtered by season
        :param season:
        :return:
        '''
        import src.application.Domain.Team as Team

        if not season:
            season = ""

        try:
            return Cache.get_element(str(self.id)+"_"+season, "TEAMS_BY_LEAGUE")
        except KeyError:
            pass

        teams_api_id = []
        query = "SELECT distinct(home_team_api_id) FROM Match WHERE league_id='" + str(self.id) + "'"
        if season != "":
            query += " AND season='"+season+"'"
        for sqllite_row in SQLLite.get_connection().execute_query(query):
            teams_api_id.append(sqllite_row[0])

        teams = []
        for team_api_id in teams_api_id:
            teams.append(Team.read_by_team_api_id(team_api_id=team_api_id))

        Cache.add_element(str(self.id)+"_"+season, teams, "TEAMS_BY_LEAGUE")
        return teams

    def get_teams_current_season(self):
        return self.get_teams(util.get_current_season())

    def add_name(self, new_league_name):
        names = self.name+"|"+new_league_name
        update = "UPDATE League set name = '"+names+"' where id='"+str(self.id)+"'"
        SQLLite.get_connection().execute_query(update)


def read_all():
    '''
    Return all the leagues
    :return:
    '''
    league_list = []
    for p in SQLLite.read_all("League"):
        league = League(p["id"])
        for attribute, value in p.items():
            league.__setattr__(attribute, value)
        league_list.append(league)
    return league_list

def read_by_country(country_id):
    '''
    Return the league in the country identified by country_id
    :param country_id:
    :return:
    '''
    try:
        return Cache.get_element(country_id,"LEAGUE_BY_COUNTRY")
    except KeyError:
        pass

    sqllite_row = SQLLite.get_connection().select("League", **{"country_id": country_id})[0]
    league = League(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        league.__setattr__(attribute, value)
    Cache.add_element(league.id, league, "LEAGUE_BY_ID")
    Cache.add_element(country_id, league, "LEAGUE_BY_COUNTRY")
    return league


def read_by_id(id):
    '''
    Return the league in the country identified by country_id
    :param country_id:
    :return:
    '''
    try:
        return Cache.get_element(id,"LEAGUE_BY_ID")
    except KeyError:
        pass

    sqllite_row = SQLLite.get_connection().select("League", **{"id": id})[0]
    league = League(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        league.__setattr__(attribute, value)
    Cache.add_element(league.id, league, "LEAGUE_BY_ID")
    Cache.add_element(league.country_id, league, "LEAGUE_BY_COUNTRY")
    return league

def read_by_name(name):
    '''
    Return the league with this name
    :param country_id:
    :return:
    '''
    try:
        return Cache.get_element(name,"LEAGUE_BY_NAME")
    except KeyError:
        pass

    try:
        sqllite_row = SQLLite.get_connection().select_like("League", **{"name": name})[0]
    except IndexError:
        return None
    league = League(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        league.__setattr__(attribute, value)
    Cache.add_element(name, league, "LEAGUE_BY_NAME")
    return league

def add_names(league_names):
    for league_id, name in league_names.items():
        league = read_by_id(league_id)
        if name not in league.name:
            league.add_name(name)


'''
# Example for league to be updated
leauge_to_update = {1:"Belgian Jupiler Pro League",
1729:"English Premier League",
4769:"French Ligue 1",
7809:"German 1. Bundesliga",
13274:"Holland Eredivisie",
15722:"Polish T-Mobile Ekstraklasa",
17642:"Portuguese Primeira Liga",
19694:"Scottish Premiership",
21518:"Spanish Primera Division",
24558:"Swiss Super League",
10257:"Italian Serie A"}

add_names(leauge_to_update)
'''