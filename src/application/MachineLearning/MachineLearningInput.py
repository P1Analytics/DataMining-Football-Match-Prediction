import numpy as np
import src.application.Domain.League as League
import src.application.Domain.Team as Team

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

def team_form(league_name, representation, n=None, season=None):
    print("team_form, representation:", representation)
    league = League.read_by_name(league_name)[0]
    matches = []
    labels = []
    matches_names = []

    for match in league.get_matches(season=season):
        if n and match.stage <= n or match.stage==1:
            continue
        home_team = match.get_home_team()
        away_team = match.get_away_team()

        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        else:
            labels.append(0)
        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

        home_form, home_n = home_team.get_points_by_season_and_stage(season, match.stage, n=n)
        away_form, away_n = away_team.get_points_by_season_and_stage(season, match.stage, n=n)

        if representation == 1:
            # Numeric values of the team forms, normalized to interval [0,3]
            matches.append(np.asarray([home_form / home_n, away_form / away_n]))

        elif representation == 2:
            # Numeric values of the team forms, normalized to interval [0,3]
            matches.append(np.asarray([home_form // home_n, away_form // away_n]))

        elif representation == 3:
            # subtracted value between the home team form and away team form. This subtracted value is normalized to the interval [-3,3]
            matches.append(np.asarray([home_form / home_n - away_form / away_n]))

        elif representation == 4:
            # discretized values of r3
            matches.append(np.asarray([home_form // home_n - away_form // away_n]))

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names

def team_home_away_form(league_name, representation, n=None, season=None):
    print("team_home_away_form, representation:", representation)
    league = League.read_by_name(league_name)[0]
    matches = []
    labels = []
    matches_names = []

    for match in league.get_matches(season=season):
        if n and match.stage <= n or match.stage==1:
            continue
        home_team = match.get_home_team()
        away_team = match.get_away_team()

        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        else:
            labels.append(0)
        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

        home_form, home_n = home_team.get_points_by_season_and_stage(season, match.stage, n=n)
        home_team_home_form, home_n1 = home_team.get_home_points_by_season_and_stage(season, match.stage, n=n)
        home_team_away_form, home_n2 = home_team.get_away_points_by_season_and_stage(season, match.stage, n=n)

        away_form, away_n = away_team.get_points_by_season_and_stage(season, match.stage, n=n)
        away_team_home_form, away_n1 = away_team.get_home_points_by_season_and_stage(season, match.stage, n=n)
        away_team_away_form, away_n2 = away_team.get_away_points_by_season_and_stage(season, match.stage, n=n)

        if representation == 1:
            # Numeric values of the team forms, normalized to interval [0,3]
            matches.append(np.asarray([home_form / home_n, home_team_home_form / home_n1, home_team_away_form / home_n2,
                                       away_form / away_n, away_team_home_form / away_n1, away_team_away_form / away_n2]))

        elif representation == 2:
            # Numeric values of the team forms, normalized to interval [0,3]
            matches.append(np.asarray([home_form // home_n, home_team_home_form // home_n1, home_team_away_form // home_n2,
                                       away_form // away_n, away_team_home_form // away_n1, away_team_away_form // away_n2]))


        elif representation == 3:
            # subtracted value between the home team form and away team form. This subtracted value is normalized to the interval [-3,3]
            matches.append(np.asarray([home_form / home_n - away_form / away_n,
                                       home_team_home_form / home_n1 - away_team_home_form / away_n1,
                                       home_team_away_form / home_n2 - away_team_away_form / away_n2]))

        elif representation == 4:
            # discretized values of r3
            matches.append(np.asarray([home_form // home_n - away_form // away_n,
                                       home_team_home_form // home_n1 - away_team_home_form // away_n1,
                                       home_team_away_form // home_n2 - away_team_away_form // away_n2]))

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names

def match_statistics(league_name, n=None, season=None):
    print("match_statistics")
    league = League.read_by_name(league_name)[0]
    matches = []
    labels = []
    matches_names = []

    for match in league.get_matches(season=season):
        if n and match.stage <= n or match.stage==1:
            continue

        home_team = match.get_home_team()
        away_team = match.get_away_team()

        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        else:
            labels.append(0)
        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

        # Goals: The subtracted difference in goals from home and away teams over 9 games.
        home_goal_done, home_goal_received = home_team.get_goals_by_season_and_stage(season, match.stage, n=n)
        home_goal = home_goal_done - home_goal_received
        away_goal_done, away_goal_received = home_team.get_goals_by_season_and_stage(season, match.stage, n=n)
        away_goal = away_goal_done - away_goal_received

        # Shots: The subtracted difference in shots from home and away teams over 9 games.
        home_shoton = home_team.get_shots(season, match.stage, n=n, on=True)
        home_shotoff = home_team.get_shots(season, match.stage, n=n, on=False)
        away_shoton = away_team.get_shots(season, match.stage, n=n, on=True)
        away_shotoff = away_team.get_shots(season, match.stage, n=n, on=False)

        # Goals ration
        home_goal_ratio = home_goal_done / (home_shoton + home_shotoff)
        away_goal_ratio = away_goal_done / (away_shoton + away_shotoff)

        # Form
        home_form, home_n = home_team.get_points_by_season_and_stage(season, match.stage, n=n)
        away_form, away_n = away_team.get_points_by_season_and_stage(season, match.stage, n=n)

        matches.append(np.asarray([home_goal, away_goal, home_shoton, away_shotoff, home_goal_ratio, away_goal_ratio, home_form, away_form]))


    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names