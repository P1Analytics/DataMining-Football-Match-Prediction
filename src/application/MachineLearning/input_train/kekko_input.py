import numpy as np
import src.util.MLUtil as MLUtil
from src.application.Exception.MLException import MLException


def kekko_input(domain,
                representation,
                stage_to_predict,         # number of next stage we want to predict
                season,
                stages_to_train=90,     # numebr of stages to consider
                                        # --> it define the size of the train (EX: 38 * 10 train input)
                ):

    matches = []
    matches_to_predict = []
    labels = []
    labels_to_predict = []
    matches_id = []
    matches_to_predict_id = []

    training_matches = domain.get_training_matches(season, stage_to_predict, stages_to_train)

    for match in training_matches:
        home_team = match.get_home_team()
        away_team = match.get_away_team()
        try:
            # posizione in classifica, posizione in classifica casa, posizione in classifica trasferta]
            match_as_array = get_classifica(domain, home_team, match.season, match.stage, stages_to_train)
            match_as_array.extend(get_classifica(domain, away_team, match.season, match.stage, stages_to_train))

            # last 5 matches, last 5 matches home, last 5 matches away
            match_as_array.extend(get_trend(home_team, match.stage, match.season))
            match_as_array.extend(get_trend(away_team, match.stage, match.season))

            # goal totali FATTI, goal totali SUBITI, goal fatti in casa, goal subiti in casa, goal fatti in trasferta, goal subiti in trasferta
            match_as_array.extend(get_goals(home_team, match.stage, match.season, stages_to_train))
            match_as_array.extend(get_goals(away_team, match.stage, match.season, stages_to_train))

            matches.append(np.asarray(match_as_array))
            matches_id.append(match.id)
            labels.append(MLUtil.get_label(match))

        except MLException:
            continue

    for match in [m for m in domain.get_matches(season=season) if m.stage == stage_to_predict]:
        home_team = match.get_home_team()
        away_team = match.get_away_team()

        try:
            # posizione in classifica, posizione in classifica casa, posizione in classifica trasferta]
            match_as_array = get_classifica(domain, home_team, match.season, match.stage, stages_to_train)
            match_as_array.extend(get_classifica(domain, away_team, match.season, match.stage, stages_to_train))

            # last 5 matches, last 5 matches home, last 5 matches away
            match_as_array.extend(get_trend(home_team, match.stage, match.season))
            match_as_array.extend(get_trend(away_team, match.stage, match.season))

            # goal totali FATTI, goal totali SUBITI, goal fatti in casa, goal subiti in casa, goal fatti in trasferta, goal subiti in trasferta
            match_as_array.extend(get_goals(home_team, match.stage, match.season, stages_to_train))
            match_as_array.extend(get_goals(away_team, match.stage, match.season, stages_to_train))

            matches_to_predict.append(np.asarray(match_as_array))

            labels_to_predict.append(MLUtil.get_label(match))
            matches_to_predict_id.append(match.id)

        except MLException:
            continue

    matches = np.asarray(matches)
    matches_to_predict = np.asarray(matches_to_predict)
    labels = np.asarray(labels)
    labels_to_predict = np.asarray(labels_to_predict)

    if len(matches) == 0 or len(matches_to_predict) == 0:
        raise MLException(2)

    return matches, labels, matches_id, matches_to_predict, matches_to_predict_id, labels_to_predict


def get_goals(team, match_stage, match_season, stages_to_train):
    goal_done, goal_received, n = team.get_goals_by_train_matches(match_season, match_stage, stages_to_train)
    h_goal_done, h_goal_received, h_n = team.get_goals_by_train_matches(match_season, match_stage, 5, home=True)
    a_goal_done, a_goal_received, a_n = team.get_goals_by_train_matches(match_season, match_stage, 5, home=False)

    return [goal_done/n, goal_received/n, h_goal_done/h_n, h_goal_received/h_n, a_goal_done/a_n, a_goal_received/a_n]


def get_trend(team, match_stage, match_season):
    trend = []
    trend.extend(transform_tren(team.get_trend(stage=match_stage, season=match_season)))
    trend.extend(transform_tren(team.get_trend(stage=match_stage, season=match_season, home=True)))
    trend.extend(transform_tren(team.get_trend(stage=match_stage, season=match_season, home=False)))

    if len(trend) != 15:
        raise MLException(2)

    return trend


def transform_tren(trend_str):
    trend_list = []
    for t in trend_str.split():
        if t == 'V':
            # win
            trend_list.append(1)
        elif t == 'P':
            # lost
            trend_list.append(2)
        elif t == 'X':
            # draw
            trend_list.append(0)

    return trend_list


def get_classifica(league, team, season, stage_to_predict, stages_to_train):

    pos = 1
    for points_i, team_i in league.get_training_ranking(season, stage_to_predict, stages_to_train):
        if team.id == team_i.id:
            break
        pos += 1

    home_pos = 1
    for points_i, team_i in league.get_training_ranking(season, stage_to_predict, stages_to_train, home=True):
        if team.id == team_i.id:
            break
        home_pos += 1

    away_pos = 1
    for points_i, team_i in league.get_training_ranking(season, stage_to_predict, stages_to_train, home=False):
        if team.id == team_i.id:
            break
        away_pos += 1

    return [pos, home_pos, away_pos]
