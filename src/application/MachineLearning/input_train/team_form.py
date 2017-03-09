import numpy as np

import src.util.MLUtil as ml_util
from src.application.Exception.MLException import MLException


def team_form(domain,
              representation,
              stage_to_predict,         # number of next stage we want to predict
              season,
              stages_to_train=None,     # numebr of stages to consider
                                        # --> it define the size of the train (EX: 38 * 10 train input)
              ):
    """

    :param domain:
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
    training_matches = domain.get_training_matches(season, stage_to_predict, stages_to_train)
    for match in training_matches:
        try:
            matches.append(get_team_form(match, stages_to_train, representation))
            matches_id.append(match.id)
            labels.append(ml_util.get_label(match))
        except MLException:
            continue

    for match in [m for m in domain.get_matches(season=season) if m.stage == stage_to_predict]:
        try:
            matches_to_predict.append(get_team_form(match, stages_to_train, representation))
            matches_to_predict_id.append(match.id)
            labels_to_predict.append(ml_util.get_label(match))
        except MLException:
            continue

    matches = np.asarray(matches)
    matches_to_predict = np.asarray(matches_to_predict)
    labels = np.asarray(labels)
    labels_to_predict = np.asarray(labels_to_predict)

    if len(matches) == 0 or len(matches_to_predict) == 0:
        raise MLException(2)

    return matches, labels, matches_id, matches_to_predict, matches_to_predict_id, labels_to_predict


def get_representations():
    return [1, 2, 3, 4]


def get_team_form(match, stages_to_train, representation):
    """

    :param match:
    :param stages_to_train:
    :param representation:
    :return:
    """
    home_team = match.get_home_team()
    away_team = match.get_away_team()

    home_form, home_n = home_team.get_points_by_train_matches(match.season, match.stage, stages_to_train)
    away_form, away_n = away_team.get_points_by_train_matches(match.season, match.stage, stages_to_train)

    if home_n == 0 or away_n == 0:
        raise MLException(2)
    if representation == 1:
        # Numeric values of the team forms, normalized to interval [0,3]
        return np.asarray([home_form / home_n, away_form / away_n])

    elif representation == 2:
        # Numeric values of the team forms, normalized to interval [0,3]
        return np.asarray([home_form // home_n, away_form // away_n])

    elif representation == 3:
        # subtracted value between the home team form and away team form.
        # This subtracted value is normalized to the interval [-3,3]
        return np.asarray([home_form / home_n - away_form / away_n])

    elif representation == 4:
        # discretized values of r3
        return np.asarray([home_form // home_n - away_form // away_n])

    raise MLException(5)
