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
            home_form, home_n = home_team.get_points_by_train_matches(match.season, match.stage, stages_to_train)
            away_form, away_n = away_team.get_points_by_train_matches(match.season, match.stage, stages_to_train)

            if home_n == 0 or away_n == 0:
                continue

            matches.append(get_team_form(away_form, away_n, home_form, home_n, representation))
            matches_id.append(match.id)
            labels.append(ml_util.get_label(match))
        except MLException:
            continue

    for match in [m for m in domain.get_matches(season=season) if m.stage == stage_to_predict]:
        home_team = match.get_home_team()
        away_team = match.get_away_team()

        try:
            home_form, home_n = home_team.get_points_by_train_matches(season, stage_to_predict, stages_to_train)
            away_form, away_n = away_team.get_points_by_train_matches(season, stage_to_predict, stages_to_train)

            if home_n == 0 or away_n == 0:
                continue

            matches_to_predict.append(get_team_form(away_form, away_n, home_form, home_n, representation))
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


def get_team_form(away_form, away_n, home_form, home_n, representation):
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

    return None