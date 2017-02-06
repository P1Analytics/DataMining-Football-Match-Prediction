import numpy as np
import src.application.Domain.League as League
import src.application.Domain.Team as Team

def get_datas_by_league(league_name, season=None):
    league = League.read_by_name(league_name)

    matches = []
    labels = []
    matches_names = []
    for match in league.get_matches(season=season):
        home_team = match.get_home_team()
        away_team = match.get_away_team()
        label = 0
        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        else:
            labels.append(0)
        # matches.append([goal_done[home_team.team_long_name],goal_received[home_team.team_long_name],goal_done[away_team.team_long_name],goal_received[away_team.team_long_name]])
        home_goal_done, home_goal_received = home_team.get_goals_by_season_and_stage(season, match.stage)
        # print(match.stage, home_team.team_long_name, home_goal_done, home_goal_received)
        away_goal_done, away_goal_received = away_team.get_goals_by_season_and_stage(season, match.stage)
        matches.append(np.asarray([home_goal_done / match.stage, home_goal_received / match.stage,
                                   home_team.get_points_by_season_and_stage(season, match.stage) / match.stage,
                                   away_goal_done / match.stage, away_goal_received / match.stage,
                                   away_team.get_points_by_season_and_stage(season, match.stage) / match.stage]))

        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names

def team_form(league_name, representation, n=9, season=None):
    print("team_form, representation:", representation)
    league = League.read_by_name(league_name)
    matches = []
    labels = []
    matches_names = []

    for match in league.get_matches(season=season):
        if match.stage <= n:
            continue
        home_team = match.get_home_team()
        away_team = match.get_away_team()

        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        else:
            labels.append(0)
        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

        home_form = home_team.get_points_by_season_and_stage(season, match.stage, n=n)
        away_form = away_team.get_points_by_season_and_stage(season, match.stage, n=n)

        if representation == 1:
            # Numeric values of the team forms, normalized to interval [0,3]
            matches.append(np.asarray([home_form / n, away_form / n]))

        elif representation == 2:
            # Numeric values of the team forms, normalized to interval [0,3]
            matches.append(np.asarray([home_form // n, away_form // n]))

        elif representation == 3:
            # subtracted value between the home team form and away team form. This subtracted value is normalized to the interval [-3,3]
            matches.append(np.asarray([home_form / n - away_form / n]))

        elif representation == 4:
            # discretized values of r3
            matches.append(np.asarray([home_form // n - away_form // n]))

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names

def team_home_away_form(league_name, representation, n=9, season=None):
    print("team_home_away_form, representation:", representation)
    league = League.read_by_name(league_name)
    matches = []
    labels = []
    matches_names = []

    for match in league.get_matches(season=season):
        if match.stage <= n:
            continue
        home_team = match.get_home_team()
        away_team = match.get_away_team()

        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        else:
            labels.append(0)
        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

        home_form = home_team.get_points_by_season_and_stage(season, match.stage, n=n)
        home_team_home_form, home_n1 = home_team.get_home_points_by_season_and_stage(season, match.stage, n=n)
        home_team_away_form, home_n2 = home_team.get_away_points_by_season_and_stage(season, match.stage, n=n)

        away_form = away_team.get_points_by_season_and_stage(season, match.stage, n=n)
        away_team_home_form, away_n1 = away_team.get_home_points_by_season_and_stage(season, match.stage, n=n)
        away_team_away_form, away_n2 = away_team.get_away_points_by_season_and_stage(season, match.stage, n=n)

        if representation == 1:
            # Numeric values of the team forms, normalized to interval [0,3]
            matches.append(np.asarray([home_form / n, home_team_home_form / home_n1, home_team_away_form / home_n2,
                                       away_form / n, away_team_home_form / away_n1, away_team_away_form / away_n2]))

        elif representation == 2:
            # Numeric values of the team forms, normalized to interval [0,3]
            matches.append(np.asarray([home_form // n, home_team_home_form // home_n1, home_team_away_form // home_n2,
                                       away_form // n, away_team_home_form // away_n1, away_team_away_form // away_n2]))


        elif representation == 3:
            # subtracted value between the home team form and away team form. This subtracted value is normalized to the interval [-3,3]
            matches.append(np.asarray([home_form / n - away_form / n,
                                       home_team_home_form / home_n1 - away_team_home_form / away_n1,
                                       home_team_away_form / home_n2 - away_team_away_form / away_n2]))

        elif representation == 4:
            # discretized values of r3
            matches.append(np.asarray([home_form // n - away_form // n,
                                       home_team_home_form // home_n1 - away_team_home_form // away_n1,
                                       home_team_away_form // home_n2 - away_team_away_form // away_n2]))

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names
