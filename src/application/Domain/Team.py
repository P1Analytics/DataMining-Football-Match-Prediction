import src.application.Domain.Match as Match
import src.application.Domain.Team_Attributes as Team_Attributes

import src.util.SQLLite as SQLLite
import src.util.util as util
import src.util.Cache as Cache

class Team(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        to_string = "Team "
        attributes = util.read_config_file("src/util/SQLLite.ini","Team")
        for attribute in attributes.keys():
            to_string+=attribute+": "+str(self.__getattribute__(attribute))+", "
        return to_string

    def get_matches(self, season=None, ordered=False):
        '''
        Return matches of this team
        :param season:
        :return:
        '''
        matches = list()
        matches = Match.read_matches_by_team(self.team_api_id, season)
        if ordered:
            return sorted(matches, key=lambda match: match.date)
        else:
            return matches

    def get_team_attributes(self,):
        return Team_Attributes.read_by_team_api_id(self.team_api_id)

    def get_points_by_season_and_stage(self, season, stage):
        '''
        Return the sum of the point got until the stage
        :param season:
        :param stage:
        :return:
        '''
        matches = self.get_matches(season=season, ordered=True)
        points = 0
        for match in matches:
            if match.stage > stage:
                return points
            if match.get_home_team().team_api_id == self.team_api_id:
                if match.home_team_goal > match.away_team_goal:
                    points += 3
                elif match.home_team_goal == match.away_team_goal:
                    points += 1
            else:
                if match.home_team_goal < match.away_team_goal:
                    points += 3
                elif match.home_team_goal == match.away_team_goal:
                    points += 1
        return points

    def get_goals_by_season_and_stage(self, season, stage):
        '''
        Return the sum of the goals done/received got until the stage
        :param season:
        :param stage:
        :return:
        '''
        matches = self.get_matches(season=season, ordered=True)
        goal_done = 0
        goal_received = 0
        for match in matches:
            if match.stage > stage:
                return goal_done, goal_received
            if match.get_home_team().team_api_id == self.team_api_id:
                goal_done += match.home_team_goal
                goal_received += match.away_team_goal
            else:
                goal_done += match.away_team_goal
                goal_received += match.home_team_goal

        return goal_done, goal_received


def read_all():
    '''
    Read all the teams
    :return:
    '''
    team_list = []
    for p in SQLLite.read_all("Team"):
        team = Team(p["id"])
        for attribute, value in p.items():
            team.__setattr__(attribute, value)
        team_list.append(team)
    return team_list

def read_by_team_api_id(team_api_id):
    '''
    Read from the DB the team by its team_api_id
    :param team_api_id:
    :return:
    '''

    try:
        return Cache.get_element(team_api_id, "TEAM_BY_API_ID")
    except KeyError:
        pass

    sqllite_row = SQLLite.get_connection().select("Team", **{"team_api_id": team_api_id})[0]
    team = Team(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        team.__setattr__(attribute, value)

    Cache.add_element(team_api_id, team, "TEAM_BY_API_ID")
    Cache.add_element(team.team_long_name, team, "TEAM_BY_LONG_NAME")
    return team

def read_by_name(team_long_name):
    '''
       Read from the DB the team by its name
       :param team_api_id:
       :return:
       '''

    try:
        return Cache.get_element(team_long_name, "TEAM_BY_LONG_NAME")
    except KeyError:
        pass

    sqllite_row = SQLLite.get_connection().select("Team", **{"team_long_name": team_long_name})[0]
    team = Team(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        team.__setattr__(attribute, value)

    Cache.add_element(team_long_name, team, "TEAM_BY_API_ID")
    Cache.add_element(team.team_long_name, team, "TEAM_BY_LONG_NAME")
    return team

def read_by_league_id(league_id, season=None):

    pass