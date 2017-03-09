import numpy as np
import src.util.MLUtil as MLUtil
from src.application.Exception.MLException import MLException


def match_statistics(domain,
                     representation,
                     stage_to_predict,         # number of next stage we want to predict
                     season,
                     stages_to_train=None,     # numebr of stages to consider
                                        # --> it define the size of the train (EX: 38 * 10 train input)
                     ):
    # init of important variables
    matches, matches_to_predict = [], []
    labels, labels_to_predict = [], []
    matches_id, matches_to_predict_id = [], []

    # get training matches
    training_matches = domain.get_training_matches(season, stage_to_predict, stages_to_train)

    # build training input
    for match in training_matches:
        try:
            matches.append(get_match_as_array(match, stages_to_train))
            labels.append(MLUtil.get_label(match))
            matches_id.append(match.id)
        except MLException:
            continue

    # match to predict
    for match in [m for m in domain.get_matches(season=season) if m.stage == stage_to_predict]:
        try:
            matches_to_predict.append(get_match_as_array(match, stages_to_train))
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


def get_match_as_array(match, stages_to_train):
    try:
        home_team = match.get_home_team()
        away_team = match.get_away_team()

        # Goals: The subtracted difference in goals from home and away teams over 9 games.
        home_goal_done, home_goal_received, home_num_match_considered = \
            home_team.get_goals_by_train_matches(match.season, match.stage, stages_to_train)
        home_goal = home_goal_done - home_goal_received

        away_goal_done, away_goal_received, away_num_match_considered \
            = away_team.get_goals_by_train_matches(match.season, match.stage, stages_to_train)
        away_goal = away_goal_done - away_goal_received

        # Shots: The subtracted difference in shots from home and away teams over 9 games.
        home_shoton = home_team.get_shots_by_train_matches(match.season, match.stage, stages_to_train, on=True)
        home_shotoff = home_team.get_shots_by_train_matches(match.season, match.stage, stages_to_train, on=False)
        away_shoton = away_team.get_shots_by_train_matches(match.season, match.stage, stages_to_train, on=True)
        away_shotoff = away_team.get_shots_by_train_matches(match.season, match.stage, stages_to_train, on=False)

        # Goals ratio
        if (home_shoton + home_shotoff) == 0 or (away_shoton + away_shotoff) == 0:
            raise MLException(2)
        home_goal_ratio = home_goal_done / (home_shoton + home_shotoff)
        away_goal_ratio = away_goal_done / (away_shoton + away_shotoff)

        # Form
        home_form, home_n = home_team.get_points_by_train_matches(match.season, match.stage, stages_to_train)
        away_form, away_n = away_team.get_points_by_train_matches(match.season, match.stage, stages_to_train)
        match_as_array = np.asarray(
            [home_goal, away_goal, home_shoton, away_shoton, home_goal_ratio, away_goal_ratio, home_form,
             away_form])
        return match_as_array
    except AttributeError:
        raise MLException(2)


def get_representations():
    return []
