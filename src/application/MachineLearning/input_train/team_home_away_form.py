import numpy as np
import src.util.MLUtil as MLUtil
from src.application.Exception.MLException import MLException


def team_home_away_form(league_or_team,
                        representation,
                        stage_to_predict,         # number of next stage we want to predict
                        season,
                        stages_to_train=None):
    """

    :param league_or_team:
    :param representation:
    :param stage_to_predict:
    :param season:
    :param stages_to_train:
    :return:
    """

    # init of important variables
    matches, matches_to_predict = [], []
    labels, labels_to_predict = [], []
    matches_id, matches_to_predict_id = [], []

    # get training matches
    training_matches = league_or_team.get_training_matches(season, stage_to_predict, stages_to_train)

    # build training input
    for match in training_matches:
        try:
            matches.append(get_home_away_team_form(match, stages_to_train, representation))
            matches_id.append(match.id)
            labels.append(MLUtil.get_label(match))
        except MLException:
            continue

    # match to predict
    for match in [m for m in league_or_team.get_matches(season=season) if m.stage == stage_to_predict]:
        try:
            matches_to_predict.append(get_home_away_team_form(match, stages_to_train, representation))
            matches_to_predict_id.append(match.id)
            labels_to_predict.append(MLUtil.get_label(match))
        except MLException:
            continue

    # convert some data srtuctures to be run
    matches = np.asarray(matches)
    matches_to_predict = np.asarray(matches_to_predict)
    labels = np.asarray(labels)
    labels_to_predict = np.asarray(labels_to_predict)

    # if there is nothing to train or notingh to predict, raise an MLExcpetion
    if len(matches) == 0 or len(matches_to_predict) == 0 or len(set([x for x in labels]))==1:
        raise MLException(2)

    return matches, labels, matches_id, matches_to_predict, matches_to_predict_id, labels_to_predict


def get_home_away_team_form(match, stages_to_train, representation):
    home_team = match.get_home_team()
    away_team = match.get_away_team()

    home_form, home_n = home_team.get_points_by_train_matches(match.season, match.stage, stages_to_train)
    away_form, away_n = away_team.get_points_by_train_matches(match.season, match.stage, stages_to_train)

    home_team_home_form, home_n1 = home_team.get_points_by_train_matches(match.season, match.stage, stages_to_train,
                                                                         home=True)
    home_team_away_form, home_n2 = home_team.get_points_by_train_matches(match.season, match.stage, stages_to_train,
                                                                         home=False)

    away_team_home_form, away_n1 = away_team.get_points_by_train_matches(match.season, match.stage, stages_to_train,
                                                                         home=True)
    away_team_away_form, away_n2 = away_team.get_points_by_train_matches(match.season, match.stage, stages_to_train,
                                                                         home=False)

    if home_n == 0 or home_n1 == 0 or home_n2 == 0 or away_n == 0 or away_n1 == 0 or away_n2 == 0:
        raise MLException(1)

    if representation == 1:
        # Numeric values of the team forms, normalized to interval [0,3]
        return np.asarray([home_form / home_n, home_team_home_form / home_n1, home_team_away_form / home_n2,
                           away_form / away_n, away_team_home_form / away_n1, away_team_away_form / away_n2])

    elif representation == 2:
        # Numeric values of the team forms, normalized to interval [0,3]
        return np.asarray([home_form // home_n, home_team_home_form // home_n1, home_team_away_form // home_n2,
                           away_form // away_n, away_team_home_form // away_n1, away_team_away_form // away_n2])

    elif representation == 3:
        # subtracted value between the home team form and away team form. This subtracted value is normalized to the interval [-3,3]
        return np.asarray([home_form / home_n - away_form / away_n,
                           home_team_home_form / home_n1 - away_team_home_form / away_n1,
                           home_team_away_form / home_n2 - away_team_away_form / away_n2])

    elif representation == 4:
        # discretized values of r3
        return np.asarray([home_form // home_n - away_form // away_n,
                           home_team_home_form // home_n1 - away_team_home_form // away_n1,
                           home_team_away_form // home_n2 - away_team_away_form // away_n2])

    raise MLException(5)

def get_representations():
    return [1, 2, 3, 4]
