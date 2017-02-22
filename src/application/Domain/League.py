import src.application.Domain.Match as Match
import src.util.util as util
import src.util.Cache as Cache
import src.util.SQLLite as SQLLite

import logging
import operator

from src.application.Exception.MLException import MLException


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

    def get_ranking(self, season):
        import src.application.Domain.Team as Team

        matches = self.get_matches(season=season)
        teams = self.get_teams(season=season)
        ranking = {team.id: 0 for team in teams}
        for m in matches:
            winner = m.get_winner()
            if not util.is_None(winner):
                ranking[winner.id] += 3
            else:
                ranking[m.get_home_team().id] += 1
                ranking[m.get_away_team().id] += 1

        ranking_ret = []
        for team, p in sorted(ranking.items(), key=operator.itemgetter(1))[::-1]:
            ranking_ret.append((p, Team.read_by_id(team)))

        return ranking_ret

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
        for sqllite_row in SQLLite.get_connection().execute_select(query):
            seasons.append(sqllite_row[0])

        Cache.add_element(self.id, seasons, "SEASONS_BY_LEAGUE")
        return seasons

    def get_matches(self,season=None, ordered = True, date=None, finished=True):
        matches = Match.read_matches_by_league(self.id, season)

        if ordered:
            matches = sorted(matches, key=lambda match: match.stage)

        if finished:
            matches = [m for m in matches if m.is_finished()]

        if date:
            matches = [m for m in matches if m.date.startswith(date)]

        return matches

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
        for sqllite_row in SQLLite.get_connection().execute_select(query):
            teams_api_id.append(sqllite_row[0])

        teams = []
        for team_api_id in teams_api_id:
            team = Team.read_by_team_api_id(team_api_id=team_api_id)
            if not util.is_None(team):
                teams.append(team)

        Cache.add_element(str(self.id)+"_"+season, teams, "TEAMS_BY_LEAGUE")
        return teams

    def get_teams_current_season(self):
        return self.get_teams(util.get_current_season())

    def get_training_matches(self, season, stage_to_predict, stages_to_train, consider_last=False):
        if util.is_None(stages_to_train):
            # stages to train not defined --> return only stage of this season
            return [m for m in self.get_matches(season=season, ordered=True) if m.stage < stage_to_predict]
        else:
            # stages to train is defined --> return number this number of stages, also for past season
            if consider_last:
                # start to consider matches of previous seasons --> take them in the reverse order
                training_matches = [m for m in self.get_matches(season=season, ordered=True)]
                training_matches = training_matches[::-1]
            else:
                training_matches = [m for m in self.get_matches(season=season, ordered=True) if
                                    m.stage < stage_to_predict]

            if len(training_matches) == 0 and stage_to_predict != 1:
                raise MLException(0)

            stages_training = set([(m.stage, m.season) for m in training_matches])
            while len(stages_training) < stages_to_train:
                # need more matches from the past season, considering the last matches
                past_training_matches = self.get_training_matches(util.get_previous_season(season),
                                                                0,
                                                                stages_to_train - len(stages_training),
                                                                consider_last=True)

                training_matches.extend(past_training_matches)
                stages_training = set([(m.stage, m.season) for m in training_matches])

            if len(training_matches) / 10 > stages_to_train:
                # too matches in training --> remove too far
                if consider_last:
                    return training_matches[:stages_to_train * 10][::-1]
                else:
                    return training_matches[-stages_to_train * 10:]

            return training_matches

    def add_name(self, new_league_name):
        names = self.name+"|"+new_league_name
        update = "UPDATE League set name = '"+names+"' where id='"+str(self.id)+"'"
        SQLLite.get_connection().execute_update(update)


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
    sqllite_rows = SQLLite.get_connection().select("League", **{"country_id": country_id})

    league_list = []
    for p in sqllite_rows:
        league = League(p["id"])
        for attribute, value in p.items():
            league.__setattr__(attribute, value)
        league_list.append(league)
    return league_list


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

def read_by_name(name, like=False):
    '''
    Return the league with this name
    :param country_id:
    :return:
    '''
    if like:
        sqllite_row = SQLLite.get_connection().select_like("League", **{"name": name})
    else:
        sqllite_row = SQLLite.get_connection().select("League", **{"name": name})

    leagues = []
    for p in sqllite_row:
        league = League(p["id"])
        for attribute, value in p.items():
            league.__setattr__(attribute, value)
        leagues.append(league)

    return leagues

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
