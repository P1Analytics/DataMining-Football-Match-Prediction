import logging
import src.util.SQLLite as SQLLite
import src.util.util as util
import src.util.Cache as Cache
import src.application.Domain.Match as Match
import src.application.Domain.Team_Attributes as Team_Attributes
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
        """
        return a list of n labels which corresponds to the last n matches result of this team
        V : win
        P : lost
        X : draw
        :param stage:
        :param season:
        :param n:
        :param home:
        :return:
        """

        matches = self.get_training_matches(season, stage, n, home=home)

        trend = ""
        for match in matches[-n:]:

            result, winner = match.get_winner()
            if util.is_None(winner):
                trend = "X " + trend

            elif winner.team_api_id == self.team_api_id:
                trend = "V "+trend

            else:
                trend = "P "+trend

        return trend

    def get_matches(self, season=None, ordered=False, finished=False, home=None):
        """
        Return matches of this team
        :param season:
        :param ordered:
        :param finished:
        :param home:
        :return:
        """
        if util.is_None(home):
            # match when team plays both home and away
            matches = Match.read_matches_by_team(self.team_api_id, season)
        elif home:
            # match when team plays home
            matches = Match.read_matches_by_home_team(self.team_api_id, season)
        else:
            # match when team plays away
            matches = Match.read_matches_by_away_team(self.team_api_id, season)

        if ordered:
            # order the match by date
            matches = sorted(matches, key=lambda match: match.date)

        if finished:
            # consider only finished matxh
            matches = [m for m in matches if m.is_finished()]

        return matches

    def get_last_team_attributes(self):
        """
        Return the last team attributes saved
        :return:
        """
        max_date = "0000-00-00"
        last_team_attributes = None

        for team_attributes in self.get_team_attributes():
            if team_attributes.date > max_date:
                max_date = team_attributes.date
                last_team_attributes = team_attributes

        return last_team_attributes

    def get_team_attributes(self):
        """
        return the list of team-attributes of this team
        :return:
        """
        return Team_Attributes.read_by_team_fifa_api_id(self.team_fifa_api_id)

    def get_points_by_train_matches(self, season, stage_to_predict, stages_to_train, home=None):
        """
        return the the tuple (points, n) where
            - points: sum of the points gathered
            - n: number of matches used to get points
        :param season:
        :param stage_to_predict:
        :param stages_to_train:
        :param home:
        :return:
        """
        matches = self.get_training_matches(season, stage_to_predict, stages_to_train, home=home)
        points = 0
        for match in matches:
            if match.home_team_goal == match.away_team_goal:
                points += 1
            elif (match.home_team_api_id == self.team_api_id and match.home_team_goal > match.away_team_goal)   \
                    or (match.away_team_api_id == self.team_api_id and match.home_team_goal < match.away_team_goal):
                points += 3

        return points, len(matches)

    def get_goals_by_train_matches(self, season, stage_to_predict, stages_to_train, home=None):
        """
        Return the sum of the goals done/received got until the stage
        Do not consider the stage in input
        If set, consider only the last n matches
        :param season:
        :param stage_to_predict:
        :param stages_to_train:
        :param home:
        :return:
        """
        matches = self.get_training_matches(season, stage_to_predict, stages_to_train, home=home)
        goal_done = 0
        goal_received = 0
        for i, match in enumerate(matches):
            # team plays hoe
            if match.home_team_api_id == self.team_api_id:
                goal_done += match.home_team_goal
                goal_received += match.away_team_goal
            # team plays away
            else:
                goal_done += match.away_team_goal
                goal_received += match.home_team_goal

        return goal_done, goal_received, len(matches)

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
        matches = self.get_matches(season=season, ordered=True, home=home, finished=True)
        if n:
            i = 0
            for match in matches:
                if match.stage >= stage:
                    break
                i += 1
            matches = matches[i-n: i]
        goal_done = 0
        goal_received = 0
        n = 0
        for match in matches:
            if match.stage >= stage:
                return goal_done, goal_received, n
            n += 1
            # team plays hoe
            if match.home_team_api_id == self.team_api_id:
                goal_done += match.home_team_goal
                goal_received += match.away_team_goal
            # team plays away
            else:
                goal_done += match.away_team_goal
                goal_received += match.home_team_goal

        return goal_done, goal_received, n

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
            if match.home_team_api_id == self.team_api_id:
                goal_done += match.home_team_goal
                goal_received += match.away_team_goal
            else:
                goal_done += match.away_team_goal
                goal_received += match.home_team_goal

        return goal_done, goal_received

    def get_assist_by_season_and_stage(self, season=None, stage=None):
        """
        Return the overall assists done by this team
        :param season:
        :param stage:
        :return:
        """
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

    def get_shots_by_train_matches(self, season, stage_to_predict, stages_to_train, on=True, home=None):
        """
        Return the number of shot(either on or off) done by this team.
        If n, it considers only the last n matches.
        If home, just when this team plays at home.
        :param season:
        :param stage_to_predict:
        :param stages_to_train:
        :param on:
        :param home:
        :return:
        """
        matches = self.get_training_matches(season, stage_to_predict, stages_to_train, home=home)
        n_shot = 0
        for match in matches:
            for shot in match.get_shots(on):
                try:
                    if shot.team == self.team_api_id:
                        n_shot += 1
                except AttributeError:
                    logging.debug("Shot of the Match with api_id [ "+str(match.match_api_id)+" ] has no attribute team")
        return n_shot

    def get_shots(self, season, stage, n=None, on=True):
        """
        Return the number of shot(either on or off) done of this team
        If n, it considers only the last n matches.

        :param season:
        :param stage:
        :param n:
        :param on:
        :return:
        """
        matches = self.get_matches(season=season, ordered=True)
        shot_on_off = 0
        for match in matches:
            if match.stage >= stage:
                return shot_on_off
            if n and match.stage < stage-n:
                continue

            for shot in match.get_shots(on):
                try:
                    if shot.team == self.team_api_id:
                        shot_on_off += 1
                except AttributeError:
                    logging.debug("Shot of the Match with api_id [ "+str(match.match_api_id)+" ] has no attribute team")

        return shot_on_off

    def get_players(self, season=None):
        """
        Return all players that played in this team
        if season, return the players for that season
        :param season:
        :return:
        """
        import src.application.Domain.Player as Player
        return Player.read_by_team_api_id(self.team_api_id, season)

    def get_current_players(self):
        """
        Return a list of players that play in this team in the current season
        :return:
        """
        return self.get_players(season=util.get_current_season())

    def get_training_matches(self, season, stage_to_predict, stages_to_train, consider_last=False, home=None):
        """
        Return a list of matches to be trained by the machine learning algorithms
        :param season:
        :param stage_to_predict: it's the stage we want to predict, or 0 in a recursive call when matches of the past
                                 season are needed
        :param stages_to_train: number of stages we need to be gathered
        :param consider_last: True if we are in a recursive call.
        :param home: consider in the train matches home/away/both
        :return:
        """
        if util.is_None(stages_to_train):
            # stages to train not defined --> return only stage of this season
            training_matches = [m for m in self.get_matches(season=season, ordered=True, home=home, finished=True)
                                if m.stage < stage_to_predict]
            if len(training_matches) == 0 and stage_to_predict == 1:
                raise MLException(0)
            else:
                return training_matches

        else:
            # stages to train is defined --> return number of stages_to_train matches, also regarding past season
            if consider_last:
                # consider last matches
                training_matches = [m for m in self.get_matches(season=season, ordered=True, finished=True, home=home)]
                training_matches = training_matches[::-1]

                if len(training_matches) == 0 and season < '2006/2007':
                    raise MLException(1)
            else:
                training_matches = [m for m in self.get_matches(season=season, ordered=True, finished=True, home=home)
                                    if not util.is_None(m.stage) and m.stage < stage_to_predict]

            stages_training = set([(m.stage, m.season) for m in training_matches])
            if len(stages_training) < stages_to_train:
                # need more matches from the past season, considering the last matches
                past_training_matches = self.get_training_matches(util.get_previous_season(season),
                                                                  0,
                                                                  stages_to_train - len(stages_training),
                                                                  consider_last=True)
                training_matches.extend(past_training_matches)

            if len(training_matches) > stages_to_train:
                # too matches in training --> remove too far
                if consider_last:
                    return training_matches[:stages_to_train][::-1]
                else:
                    return training_matches[-stages_to_train:]

            return training_matches

    def save_team_attributes(self, team_attributes):
        """

        :param team_attributes:
        :return:
        """
        Team_Attributes.write_team_attributes(self, team_attributes)


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


def read_teams_by_league(league, season=None):
    """
    return the teams playing in a league, within a season as optional parameter
    :param league:
    :param season:
    :return:
    """
    if not season:
        season = ""

    try:
        return Cache.get_element(str(league.id) + "_" + season, "TEAMS_BY_LEAGUE")
    except KeyError:
        pass

    teams_api_id = []
    query = "SELECT distinct(home_team_api_id) FROM Match WHERE league_id='" + str(league.id) + "'"
    if season != "":
        query += " AND season='" + season + "'"
    for sqllite_row in SQLLite.get_connection().execute_select(query):
        teams_api_id.append(sqllite_row[0])

    teams = []
    for team_api_id in teams_api_id:
        if not util.is_None(team_api_id):
            team = read_by_team_api_id(team_api_id=team_api_id)
            if not util.is_None(team):
                teams.append(team)

    Cache.add_element(str(league.id) + "_" + season, teams, "TEAMS_BY_LEAGUE")
    return teams


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
    Cache.add_element(team.team_api_id, team, "TEAM_BY_API_ID")
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
    Cache.add_element(team.team_api_id, team, "TEAM_BY_API_ID")
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
    """
    Remove the team from the cache, and delete it from the DB
    :param team:
    :return:
    """
    Cache.del_element(team.id, "TEAM_BY_ID")
    Cache.del_element(team.team_api_id, "TEAM_BY_API_ID")
    Cache.del_element(team.team_long_name, "TEAM_BY_LONG_NAME")
    Cache.del_element(team.team_fifa_api_id, "TEAM_BY_FIFA_API_ID")

    SQLLite.get_connection().delete("Team", team)


def write_new_team(team_long_name, team_fifa_api_id, team_api_id=None, team_short_name=None):
    """
    Write a new team in the DB
    :param team_long_name:
    :param team_fifa_api_id:
    :param team_api_id:
    :param team_short_name:
    :return:
    """
    team_diz = dict()
    team_diz["team_long_name"] = team_long_name

    if not util.is_None(team_fifa_api_id):
        team_diz["team_fifa_api_id"] = team_fifa_api_id
    if not util.is_None(team_api_id):
        team_diz["team_api_id"] = team_api_id
    if not util.is_None(team_short_name):
        team_diz["team_short_name"] = team_short_name

    SQLLite.get_connection().insert("Team", team_diz)
    if not util.is_None(team_fifa_api_id):
        return read_by_team_fifa_api_id(team_fifa_api_id)
    elif not util.is_None(team_api_id):
        return read_by_team_api_id(team_api_id)
    else:
        return None


def update(team):
    """
    Update the team in the DB, and return its version updated
    :param team:
    :return:
    """
    SQLLite.get_connection().update("Team", team)

    Cache.del_element(team.id, "TEAM_BY_ID")
    Cache.del_element(team.team_api_id, "TEAM_BY_API_ID")
    Cache.del_element(team.team_long_name, "TEAM_BY_LONG_NAME")
    Cache.del_element(team.team_fifa_api_id, "TEAM_BY_FIFA_API_ID")

    return read_by_id(team.id)


def merge(team1, team2):
    """
    Merge two teams that identifie the same one
    :param team1:
    :param team2:
    :return:
    """
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
