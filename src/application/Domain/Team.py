import logging

import src.application.Domain.Match as Match
import src.application.Domain.Player as Player
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
        matches = Match.read_matches_by_team(self.team_api_id, season)
        if ordered:
            return sorted(matches, key=lambda match: match.date)
        else:
            return matches

    def get_home_matches(self, season=None, ordered=False):
        '''
        Return home matches of this team
        :param season:
        :return:
        '''
        matches = Match.read_matches_by_home_team(self.team_api_id, season)
        if ordered:
            return sorted(matches, key=lambda match: match.date)
        else:
            return matches

    def get_away_matches(self, season=None, ordered=False):
        '''
        Return home matches of this team
        :param season:
        :return:
        '''
        matches = Match.read_matches_by_away_team(self.team_api_id, season)
        if ordered:
            return sorted(matches, key=lambda match: match.date)
        else:
            return matches

    def get_last_team_attributes(self):
        max_date = "0000-00-00"
        last_team_attributes = None

        for team_attributes in self.get_team_attributes():
            if team_attributes.date > max_date:
                max_date = team_attributes.date
                last_team_attributes = team_attributes

        return last_team_attributes


    def get_team_attributes(self, date=None):
        return Team_Attributes.read_by_team_fifa_api_id(self.team_fifa_api_id)

    def get_current_team_attributes(self):
        return self.get_team_attributes(util.get_today_date())

    def get_points_by_season_and_stage(self, season, stage, n=None):
        '''
        Return the sum of the point got until the stage
        Do not considere the stage in input
        If n is set, consider only the last n matches
        :param season:
        :param stage:
        :return:
        '''
        matches = self.get_matches(season=season, ordered=True)
        points = 0
        match_used = 0
        for match in matches:
            if match.stage >= stage:
                return points, match_used
            if n and match.stage < stage - n:
                continue
            match_used += 1
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
        return points, match_used

    def get_home_points_by_season_and_stage(self, season, stage, n=None):
        '''
        Return the sum of the home point got until the stage
        Do not considere the stage in input
        If n is set, consider only the last n matches
        :param season:
        :param stage:
        :return: points, number of matches considered
        '''
        matches = self.get_home_matches(season=season, ordered=True)
        previous_matches = []
        for match in matches:
            if match.stage >= stage:
                break
            previous_matches.append(match)
        if n:
            matches = previous_matches[-n:]

        points = 0
        match_used = 0
        for match in matches:
            match_used += 1
            if match.home_team_goal > match.away_team_goal:
                points += 3
            elif match.home_team_goal == match.away_team_goal:
                points += 1

        return points, match_used

    def get_away_points_by_season_and_stage(self, season, stage, n=None):
        '''
        Return the sum of the away points got until the stage
        Do not considere the stage in input
        If n is set, consider only the last n matches
        :param season:
        :param stage:
        :return: points, number of matches considered
        '''
        matches = self.get_away_matches(season=season, ordered=True)
        previous_matches = []
        for match in matches:
            if match.stage >= stage:
                break
            previous_matches.append(match)
        if n:
            matches = previous_matches[-n:]

        points = 0
        match_used = 0
        for match in matches:
            match_used += 1
            if match.home_team_goal < match.away_team_goal:
                points += 3
            elif match.home_team_goal == match.away_team_goal:
                points += 1

        return points, match_used

    def get_goals_by_season_and_stage(self, season, stage, n=None):
        '''
        Return the sum of the goals done/received got until the stage
        Do not considere the stage in input
        If set, consider only the last n matches
        :param season:
        :param stage:
        :param n:
        :return:
        '''
        matches = self.get_matches(season=season, ordered=True)
        goal_done = 0
        goal_received = 0
        for match in matches:
            if match.stage >= stage:
                return goal_done, goal_received
            if n and match.stage < stage-n:
                continue
            if match.get_home_team().team_api_id == self.team_api_id:
                goal_done += match.home_team_goal
                goal_received += match.away_team_goal
            else:
                goal_done += match.away_team_goal
                goal_received += match.home_team_goal

        return goal_done, goal_received

    def get_shots(self, season, stage, n=None, on=True):
        '''
        Return the shoton done of this team
        If n, it considers only the last n matches.
        :param season:
        :param stage:
        :param n:
        :return:
        '''
        matches = self.get_matches(season=season, ordered=True)
        shoton = 0
        for match in matches:
            if match.stage >= stage:
                return shoton
            if n and match.stage < stage-n:
                continue

            for shot in match.get_shots(on):
                try:
                    if shot.team == self.team_api_id:
                        shoton += 1
                except AttributeError:
                    logging.debug("Shot of the Match with api_id [ "+str(match.match_api_id)+" ] has no attribute team")

        return shoton


    def get_players(self, season = None):
        '''
        Return all players that played in this team
        if season, return the players for that season
        :param season:
        :return:
        '''
        return Player.read_by_team_api_id(self.team_api_id, season)


    def get_current_players(self):
        '''
        Return a list of players that play in this team in the current season
        :return:
        '''
        return self.get_players(season = util.get_current_season())


    def save_team_attributes(self, team_attributes, force=False):
        Team_Attributes.write_team_attributes(self, team_attributes, force)

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

    try:
        sqllite_row = SQLLite.get_connection().select("Team", **{"team_api_id": team_api_id})[0]
    except IndexError:
        return None
    team = Team(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        team.__setattr__(attribute, value)

    Cache.add_element(team_api_id, team, "TEAM_BY_API_ID")
    Cache.add_element(team.team_long_name, team, "TEAM_BY_LONG_NAME")
    Cache.add_element(team.team_fifa_api_id, team, "TEAM_BY_FIFA_API_ID")
    return team

def read_by_team_fifa_api_id(team_fifa_api_id):
    '''
    Read from the DB the team by its team_api_id
    :param team_api_id:
    :return:
    '''

    try:
        return Cache.get_element(team_fifa_api_id, "TEAM_BY_FIFA_API_ID")
    except KeyError:
        pass

    try:
        sqllite_row = SQLLite.get_connection().select("Team", **{"team_fifa_api_id": team_fifa_api_id})[0]
    except IndexError:
        return None
    team = Team(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        team.__setattr__(attribute, value)

    Cache.add_element(team.id, team, "TEAM_BY_API_ID")
    Cache.add_element(team.team_long_name, team, "TEAM_BY_LONG_NAME")
    Cache.add_element(team.team_fifa_api_id, team, "TEAM_BY_FIFA_API_ID")
    return team


def read_by_name(team_long_name, like=False):
    '''
       Read from the DB the team by its name
       :param team_api_id:
       :return:
       '''

    if like:
        sqllite_rows = SQLLite.get_connection().select_like("Team", **{"team_long_name": team_long_name})
    else:
        sqllite_rows = SQLLite.get_connection().select("Team", **{"team_long_name": team_long_name})

    teams = []
    for p in sqllite_rows:
        team = Team(p["id"])
        for attribute, value in p.items():
            team.__setattr__(attribute, value)
        teams.append(team)
    return teams


def write_new_team(team_long_name, team_fifa_api_id):
    SQLLite.get_connection().insert("Team", {"team_long_name":team_long_name, "team_fifa_api_id":team_fifa_api_id})
    return read_by_team_fifa_api_id(team_fifa_api_id)

def update(team):
    SQLLite.get_connection().update("Team", team)
    Cache.del_element(team.team_api_id, "TEAM_BY_API_ID")
    Cache.del_element(team.team_long_name, "TEAM_BY_LONG_NAME")
    Cache.del_element(team.team_fifa_api_id, "TEAM_BY_FIFA_API_ID")
