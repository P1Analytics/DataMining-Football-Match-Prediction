import logging

import src.application.Domain.Match as Match
import src.application.Domain.Player as Player
import src.application.Domain.Team_Attributes as Team_Attributes

import src.util.SQLLite as SQLLite
import src.util.util as util
import src.util.Cache as Cache

from bs4 import BeautifulSoup
from src.application.Exception.MLException import MLException


class Team(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        to_string = "Team "
        attributes = util.read_config_file("src/util/SQLLite.ini", "Team")
        for attribute in attributes.keys():
            to_string += attribute+": " + str(self.__getattribute__(attribute)) + ", "
        return to_string

    def get_trend(self, stage=None, season=None, n=5, home=None):

        matches = self.get_matches(season=season, ordered=True, finished=True, home=home)

        if stage:
            matches = [m for m in matches if m.stage < stage]

        trend = ""
        for match in matches[-n:]:
            if util.is_None(match.get_winner()):
                trend = "X " + trend
            elif match.get_winner().team_api_id == self.team_api_id:
                trend = "V "+trend
            else:
                trend = "P "+trend

        return trend

    def get_matches(self, season=None, ordered=False, finished=True, home=None):
        """
        Return matches of this team
        :param season:
        :param ordered:
        :param finished:
        :param home:
        :return:
        """
        if util.is_None(home):
            matches = Match.read_matches_by_team(self.team_api_id, season)
        elif home:
            matches = Match.read_matches_by_home_team(self.team_api_id, season)
        else:
            matches = Match.read_matches_by_away_team(self.team_api_id, season)

        if ordered:
            matches = sorted(matches, key=lambda match: match.date)

        if finished:
            matches = [m for m in matches if m.is_finished()]

        return matches

    def get_last_team_attributes(self):
        max_date = "0000-00-00"
        last_team_attributes = None

        for team_attributes in self.get_team_attributes():
            if team_attributes.date > max_date:
                max_date = team_attributes.date
                last_team_attributes = team_attributes

        return last_team_attributes

    def get_team_attributes(self):
        return Team_Attributes.read_by_team_fifa_api_id(self.team_fifa_api_id)

    def get_points_by_train_matches(self, season, stage_to_predict, stages_to_train, home=None):
        matches = self.get_training_matches(season, stage_to_predict, stages_to_train, home=home)
        points = 0
        for match in matches:
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
        return points, len(matches)

    def get_points_by_season_and_stage(self, season, stage, n=None):
        """
        Return the sum of the point got until the stage
        Do not considere the stage in input
        If n is set, consider only the last n matches
        :param season:
        :param stage:
        :param n:
        :return:
        """


        matches = self.get_matches(season=season, ordered=True)
        points = 0
        match_used = 0
        for match in matches:
            if match.stage > stage:
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
        """
        Return the sum of the home point got until the stage
        Do not considere the stage in input
        If n is set, consider only the last n matches

        :param season:
        :param stage:
        :param n:
        :return:
        """
        matches = self.get_matches(season=season, ordered=True, home=True)
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
        """
        Return the sum of the away points got until the stage
        Do not considere the stage in input
        If n is set, consider only the last n matches

        :param season:
        :param stage:
        :param n:
        :return:
        """
        matches = self.get_matches(season=season, ordered=True, home=False)
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

    def get_goals_by_season_and_stage(self, season, stage, n=None, home=None):
        """
        Return the sum of the goals done/received got until the stage
        Do not consider the stage in input
        If set, consider only the last n matches

        :param season:
        :param stage:
        :param n:
        :param home:
        :return:
        """

        matches = self.get_matches(season=season, ordered=True, home=home)
        if n:
            i = 0
            for match in matches:
                if match.stage >= stage:
                    break
                i += 1
            matches = matches[i-n: i]
        goal_done = 0
        goal_received = 0
        num_matches_considered = 0
        for match in matches:
            if match.stage >= stage:
                return goal_done, goal_received, num_matches_considered

            if not util.is_None(match.get_home_team()) \
                    and match.get_home_team().team_api_id == self.team_api_id:
                num_matches_considered += 1
                goal_done += match.home_team_goal
                goal_received += match.away_team_goal

            elif not util.is_None(match.get_away_team()) \
                    and match.get_away_team().team_api_id == self.team_api_id:
                num_matches_considered += 1
                goal_done += match.away_team_goal
                goal_received += match.home_team_goal

        return goal_done, goal_received, num_matches_considered

    def get_goals_by_season(self, season=None):
        """
        Return the sum of the goals done/received got in this season

        :param season:
        :return:
        """
        matches = self.get_matches(season=season)
        goal_done = 0
        goal_received = 0
        for match in matches:
            if match.get_home_team() and match.get_home_team().team_api_id == self.team_api_id:
                goal_done += match.home_team_goal
                goal_received += match.away_team_goal
            elif match.get_away_team() and match.get_away_team().team_api_id == self.team_api_id:
                goal_done += match.away_team_goal
                goal_received += match.home_team_goal

        return goal_done, goal_received

    def get_assist_by_season_and_stage(self, season=None, stage=None):
        cnt = 0
        for match in self.get_matches(season=season, ordered=True):
            if not util.is_None(stage) and match.stage >= stage:
                return cnt
            soup = BeautifulSoup(match.goal, "html.parser")
            for value in soup.find_all('value'):
                team = value.find('team')
                if team and int(str(team.string).strip()) == self.team_api_id:
                    if not util.is_None(value.find('player2')):
                        cnt += 1
        return cnt

    def get_shots(self, season, stage, n=None, on=True):
        """
        Return the shoton done of this team
        If n, it considers only the last n matches.

        :param season:
        :param stage:
        :param n:
        :param on:
        :return:
        """
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

    def get_players(self, season=None):
        """
        Return all players that played in this team
        if season, return the players for that season

        :param season:
        :return:
        """
        return Player.read_by_team_api_id(self.team_api_id, season)

    def get_current_players(self):
        """
        Return a list of players that play in this team in the current season

        :return:
        """
        return self.get_players(season=util.get_current_season())

    def get_training_matches(self, season, stage_to_predict, stages_to_train, consider_last=False, home=None):
        if util.is_None(stages_to_train):
            # stages to train not defined --> return only stage of this season
            return [m for m in self.get_matches(season=season, ordered=True,  home=home) if m.stage < stage_to_predict]
        else:
            # stages to train is defined --> return number this number of stages, also for past season
            if consider_last:
                # consider last matches
                training_matches = [m for m in self.get_matches(season=season, ordered=True, home=home)]
                training_matches = training_matches[::-1]

                if len(training_matches) == 0:
                    raise MLException(1)
            else:
                training_matches = [m for m in self.get_matches(season=season, ordered=True, home=home) if
                                    m.stage < stage_to_predict]

            #if len(training_matches) == 0 and stage_to_predict != 1:
                #raise MLException(1)

            stages_training = set([(m.stage, m.season) for m in training_matches])
            while len(stages_training) < stages_to_train:
                # need more matches from the past season, considering the last matches
                past_training_matches = self.get_training_matches(util.get_previous_season(season),
                                                                  0,
                                                                  stages_to_train - len(stages_training),
                                                                  consider_last=True)

                training_matches.extend(past_training_matches)
                stages_training = set([(m.stage, m.season) for m in training_matches])

            if len(training_matches) > stages_to_train:
                # too matches in training --> remove too far
                if consider_last:
                    return training_matches[:stages_to_train]
                else:
                    return training_matches[-stages_to_train:]

            return training_matches

    def save_team_attributes(self, team_attributes, force=False):
        Team_Attributes.write_team_attributes(self, team_attributes, force)


def read_all():
    """
    Read all the teams
    :return:
    """
    team_list = []
    for p in SQLLite.read_all("Team"):
        team = Team(p["id"])
        for attribute, value in p.items():
            team.__setattr__(attribute, value)
        team_list.append(team)
    return team_list


def read_by_team_api_id(team_api_id):
    """
    Read from the DB the team by its team_api_id
    :param team_api_id:
    :return:
    """

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

    Cache.add_element(team.id, team, "TEAM_BY_ID")
    Cache.add_element(team_api_id, team, "TEAM_BY_API_ID")
    Cache.add_element(team.team_long_name, team, "TEAM_BY_LONG_NAME")
    Cache.add_element(team.team_fifa_api_id, team, "TEAM_BY_FIFA_API_ID")
    return team


def read_by_team_fifa_api_id(team_fifa_api_id):
    """
    Read from the DB the team by its team_fifa_api_id
    :param team_fifa_api_id:
    :return:
    """

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

    Cache.add_element(team.id, team, "TEAM_BY_ID")
    Cache.add_element(team.team_api_id, team, "TEAM_BY_API_ID")
    Cache.add_element(team.team_long_name, team, "TEAM_BY_LONG_NAME")
    Cache.add_element(team.team_fifa_api_id, team, "TEAM_BY_FIFA_API_ID")
    return team


def read_by_id(id):
    """
    Read from the DB the team by its team_api_id
    :param id:
    :return:
    """

    try:
        return Cache.get_element(id, "TEAM_BY_ID")
    except KeyError:
        pass

    try:
        sqllite_row = SQLLite.get_connection().select("Team", **{"id": id})[0]
    except IndexError:
        return None
    team = Team(sqllite_row["id"])
    for attribute, value in sqllite_row.items():
        team.__setattr__(attribute, value)

    Cache.add_element(team.id, team, "TEAM_BY_ID")
    Cache.add_element(team.id, team, "TEAM_BY_API_ID")
    Cache.add_element(team.team_long_name, team, "TEAM_BY_LONG_NAME")
    Cache.add_element(team.team_fifa_api_id, team, "TEAM_BY_FIFA_API_ID")
    return team


def read_by_name(team_long_name, like=False):
    """
    Read from the DB the team by its name
    :param team_long_name:
    :param like:
    :return:
    """

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


def delete(team):
    SQLLite.get_connection().delete("Team", team)


def write_new_team(team_long_name, team_fifa_api_id, team_api_id=None, team_short_name=None):
    team_diz = dict()
    team_diz["team_long_name"] = team_long_name
    team_diz["team_fifa_api_id"] = team_fifa_api_id

    if team_api_id:
        team_diz["team_api_id"] = team_api_id
    if team_short_name:
        team_diz["team_short_name"] = team_short_name

    SQLLite.get_connection().insert("Team", team_diz)
    return read_by_team_fifa_api_id(team_fifa_api_id)


def update(team):
    SQLLite.get_connection().update("Team", team)
    Cache.del_element(team.team_api_id, "TEAM_BY_API_ID")
    Cache.del_element(team.team_long_name, "TEAM_BY_LONG_NAME")
    Cache.del_element(team.team_fifa_api_id, "TEAM_BY_FIFA_API_ID")


def merge(team1, team2):
    # team fifa api id
    if not util.is_None(team1.team_fifa_api_id):
        team_fifa_api_id = team1.team_fifa_api_id
    else:
        team_fifa_api_id = team2.team_fifa_api_id

    # team api id
    if not util.is_None(team1.team_api_id):
        team_api_id = team1.team_api_id
    else:
        team_api_id = team2.team_api_id

    # team long name
    team_long_name = ""
    if not util.is_None(team1.team_long_name):
        team_long_name = team1.team_long_name
    if not util.is_None(team2.team_long_name) and team2.team_long_name != team_long_name:
        if team_long_name == "":
            team_long_name = team2.team_long_name
        else:
            team_long_name += "|"+team2.team_long_name

    # team short name
    team_short_name = ""
    if not util.is_None(team1.team_short_name):
        team_short_name = team1.team_short_name
    if not util.is_None(team2.team_short_name) and team2.team_short_name != team_short_name:
        if team_short_name == "":
            team_short_name = team2.team_short_name
        else:
            team_short_name += "|"+team2.team_short_name

    delete(team1)
    delete(team2)

    team = write_new_team(team_long_name, team_fifa_api_id, team_api_id, team_short_name)
    print("Updating team, ", team)
    return team
