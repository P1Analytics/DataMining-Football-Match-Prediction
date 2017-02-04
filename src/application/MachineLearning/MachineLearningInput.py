import numpy as np
import src.application.Domain.League as League
import src.application.Domain.Team as Team

def get_datas():
    italy_league = League.read_all()[4]
    teams = italy_league.get_teams("2015/2016")

    goal_done = {team.team_long_name: 0 for team in teams}
    goal_received = {team.team_long_name: 0 for team in teams}

    matches = []
    labels = []
    matches_names = []
    for match in italy_league.get_matches(season="2015/2016"):
        home_team = match.get_home_team()
        away_team = match.get_away_team()
        label = 0
        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        else:
            labels.append(0)
        # matches.append([goal_done[home_team.team_long_name],goal_received[home_team.team_long_name],goal_done[away_team.team_long_name],goal_received[away_team.team_long_name]])
        home_goal_done, home_goal_received = home_team.get_goals_by_season_and_stage("2015/2016", match.stage)
        # print(match.stage, home_team.team_long_name, home_goal_done, home_goal_received)
        away_goal_done, away_goal_received = away_team.get_goals_by_season_and_stage("2015/2016", match.stage)
        matches.append(np.asarray([home_goal_done / match.stage, home_goal_received / match.stage,
                                   home_team.get_points_by_season_and_stage("2015/2016", match.stage) / match.stage,
                                   away_goal_done / match.stage, away_goal_received / match.stage,
                                   away_team.get_points_by_season_and_stage("2015/2016", match.stage) / match.stage]))

        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    return matches, labels, matches_names