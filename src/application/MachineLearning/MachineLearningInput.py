import numpy as np
import src.application.Domain.League as League
import src.application.Domain.Team as Team


import src.application.MachineLearning.input_train.team_form as team_form_input
import src.application.MachineLearning.input_train.team_home_away_form as team_home_away_form_input


def team_form(domain, representation, stage, stages_to_train, season):


    return team_form_input.team_form(domain,
                                         representation,
                                         stage,
                                         stages_to_train=stages_to_train,
                                         season=season)



def team_home_away_form(league, representation, stage, stages_to_train, season):
    return team_home_away_form_input.team_home_away_form(league,
                                                         representation,
                                                         stage,
                                                         stages_to_train=stages_to_train,
                                                         season=season)


def get_datas_by_league(league_name, season=None):
    league = League.read_by_name(league_name, like=True)[0]

    matches = []
    labels = []
    matches_names = []
    for match in league.get_matches(season=season):
        if match.stage == 1:
            continue
        home_team = match.get_home_team()
        away_team = match.get_away_team()
        label = 0

        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        elif match.home_team_goal < match.away_team_goal:
            labels.append(2)
        else:
            labels.append(0)

        home_goal_done, home_goal_received, home_num_match_considered = home_team.get_goals_by_season_and_stage(season, match.stage)
        away_goal_done, away_goal_received, away_num_match_considered = away_team.get_goals_by_season_and_stage(season, match.stage)
        home_team_points, home_n = home_team.get_points_by_season_and_stage(season, match.stage)
        away_team_points, away_n = away_team.get_points_by_season_and_stage(season, match.stage)

        matches.append(np.asarray([home_goal_done / match.stage, home_goal_received / match.stage,
                                   home_team_points / home_n,
                                   away_goal_done / match.stage, away_goal_received / match.stage,
                                   away_team_points / away_n]))

        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names


def get_datas_by_team(team_api_id, season = None):
    matches = []
    labels = []
    matches_names = []
    team = Team.read_by_team_fifa_api_id(team_api_id)
    for match in team.get_matches(season=season):
        if match.stage == 1:
            continue
        home_team = match.get_home_team()
        away_team = match.get_away_team()

        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        elif match.home_team_goal < match.away_team_goal:
            labels.append(2)
        else:
            labels.append(0)
        home_goal_done, home_goal_received = home_team.get_goals_by_season_and_stage(season, match.stage)
        away_goal_done, away_goal_received = away_team.get_goals_by_season_and_stage(season, match.stage)
        home_team_points, home_n = home_team.get_points_by_season_and_stage(season, match.stage)
        away_team_points, away_n = away_team.get_points_by_season_and_stage(season, match.stage)

        matches.append(np.asarray([home_goal_done / match.stage, home_goal_received / match.stage,
                                   home_team_points / home_n,
                                   away_goal_done / match.stage, away_goal_received / match.stage,
                                   away_team_points / away_n]))

        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names


def match_statistics(league, n=None, season=None):
    print("match_statistics")
    matches = []
    labels = []
    matches_names = []

    for match in league.get_matches(season=season, ordered=True):
        if n and match.stage <= n or match.stage==1:
            continue

        home_team = match.get_home_team()
        away_team = match.get_away_team()

        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        elif match.home_team_goal < match.away_team_goal:
            labels.append(2)
        else:
            labels.append(0)

        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

        # Goals: The subtracted difference in goals from home and away teams over 9 games.
        home_goal_done, home_goal_received, home_num_match_considered = home_team.get_goals_by_season_and_stage(season, match.stage, n=n)
        home_goal = home_goal_done - home_goal_received
        away_goal_done, away_goal_received, away_num_match_considered = home_team.get_goals_by_season_and_stage(season, match.stage, n=n)
        away_goal = away_goal_done - away_goal_received

        # Shots: The subtracted difference in shots from home and away teams over 9 games.
        home_shoton = home_team.get_shots(season, match.stage, n=n, on=True)
        home_shotoff = home_team.get_shots(season, match.stage, n=n, on=False)
        away_shoton = away_team.get_shots(season, match.stage, n=n, on=True)
        away_shotoff = away_team.get_shots(season, match.stage, n=n, on=False)

        # Goals ratio
        home_goal_ratio = home_goal_done / (home_shoton + home_shotoff)
        away_goal_ratio = away_goal_done / (away_shoton + away_shotoff)

        # Form
        home_form, home_n = home_team.get_points_by_season_and_stage(season, match.stage, n=n)
        away_form, away_n = away_team.get_points_by_season_and_stage(season, match.stage, n=n)

        matches.append(np.asarray([home_goal, away_goal, home_shoton, away_shoton, home_goal_ratio, away_goal_ratio, home_form, away_form]))

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names