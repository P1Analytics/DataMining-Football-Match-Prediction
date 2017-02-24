import logging
import numpy as np
import src.application.Domain.League as League
import src.application.Domain.Team as Team


import src.application.MachineLearning.input_train.team_form as team_form_input
import src.application.MachineLearning.input_train.team_home_away_form as team_home_away_form_input
import src.application.MachineLearning.input_train.match_statistics as match_statistics_input

log = logging.getLogger(__name__)


def get_input_to_train(id, domain, representation, stage, stages_to_train, season):
    if id == 1:
        log.debug("team form")
        return team_form_input.team_form(domain,
                                         representation,
                                         stage,
                                         stages_to_train=stages_to_train,
                                         season=season)
    if id == 2:
        log.debug("team home away form")
        return team_home_away_form_input.team_home_away_form(domain,
                                                             representation,
                                                             stage,
                                                             stages_to_train=stages_to_train,
                                                             season=season)

    if id == 3:
        log.debug("match statistics")
        return match_statistics_input.match_statistics(domain,
                                                       representation,
                                                       stage,
                                                       stages_to_train=stages_to_train,
                                                       season=season)

    else:
        print("The only possible choices are:")
        print("\t1: team_form")
        print("\t2: team_home_away_form")
        print("\t3: match_statistics")
        raise ValueError


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


