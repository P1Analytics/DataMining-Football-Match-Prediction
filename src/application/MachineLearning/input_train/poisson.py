import numpy as np

import src.util.MLUtil as ml_util
from src.application.Exception.MLException import MLException


def poisson_input(domain,
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
    matches_names = []
    matches_to_predict_names = []

    training_matches = domain.get_training_matches(season, stage_to_predict, stages_to_train)
    '''
    # train set
    for match in training_matches:
        home_team = match.get_home_team()
        away_team = match.get_away_team()
        try:
            matches.append(np.asarray(get_match_as_array(away_team, domain, home_team, match, season, stages_to_train)))
            matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)
            labels.append(ml_util.get_label(match))
        except MLException:
            continue
    '''
    # set to be predicted
    for match in [m for m in domain.get_matches(season=season) if m.stage == stage_to_predict]:
        home_team = match.get_home_team()
        away_team = match.get_away_team()
        try:
            matches_to_predict.append(np.asarray(get_match_as_array(away_team, domain, home_team, match, season, stages_to_train)))
            matches_to_predict_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)
            labels_to_predict.append(ml_util.get_label(match))
        except MLException:
            continue

    #if len(matches) == 0 or len(matches_to_predict) == 0:
    if len(matches_to_predict) == 0:
        raise MLException(2)

    matches = np.asarray(matches)
    matches_to_predict = np.asarray(matches_to_predict)
    labels = np.asarray(labels)
    labels_to_predict = np.asarray(labels_to_predict)

    return matches, labels, matches_names, matches_to_predict, matches_to_predict_names, labels_to_predict


def get_match_as_array(away_team, domain, home_team, match, season, stages_to_train):
    # get averages by domain
    avg_home_goal_done, avg_home_goal_rece, \
    avg_away_goal_done, avg_away_goal_rece = get_average_goals(domain, season, match.stage, stages_to_train)
    # get strength of the team, compared to averges
    home_attack_strength, home_defense_strength = get_strength(avg_home_goal_done,
                                                               avg_away_goal_rece,
                                                               home_team,
                                                               season,
                                                               match.stage,
                                                               stages_to_train,
                                                               home=True)
    away_attack_strength, away_defense_strength = get_strength(avg_away_goal_done,
                                                               avg_home_goal_rece,
                                                               away_team,
                                                               season,
                                                               match.stage,
                                                               stages_to_train,
                                                               home=False)
    # get expected number of goals two teams will score
    home_exp_goals = get_goal_expectancy(home_attack_strength, away_defense_strength, avg_home_goal_done)
    away_exp_goals = get_goal_expectancy(away_attack_strength, home_defense_strength, avg_away_goal_done)
    #print(season, match.stage, home_team.team_long_name,away_team.team_long_name)
    #print([away_exp_goals, home_exp_goals])
    return [home_exp_goals, away_exp_goals]


def get_goal_expectancy(t1_attack_strength, t2_defense_strength, average_t1_goals):
    """
    return the expected goals that t1 will score

    :param t1_attack_strength:
    :param t2_defense_strength:
    :param average_t1_goals:
    :return:
    """
    return t1_attack_strength*t2_defense_strength*average_t1_goals

def get_strength(avg_goal_done, avg_goal_rece, team, season, stage, stages_to_train, home=True):
    """
    return the attack strength and the defence strength of a team,
    computed by comparing its characteristic against the average

    :param avg_goal_done: average goals done
    :param avg_goal_rece: average goals received
    :param team:
    :param season:
    :param stage:
    :param stages_to_train:
    :param home:
    :return:
    """
    team_goal_done, team_goal_rece, n = team.get_goals_by_train_matches(season, stage, stages_to_train, home=home)

    return (team_goal_done / n) / avg_goal_done, (team_goal_rece / n) / avg_goal_rece


def get_average_goals(league, season, stage, stages_to_train):
    """
    return the average home goal done (eqauls to away goal received)
    and home goal receives (equals to away goals done)
    based on the number of the training matches
    :param league:
    :param season:
    :param stage:
    :param stages_to_train:
    :return:
    """
    matches = league.get_training_matches(season, stage, stages_to_train)
    home_goal_done = 0          # equals to away_goal_receive
    home_goal_rece = 0      # equals to away_goal_done
    for match in matches:
        home_goal_done += match.home_team_goal
        home_goal_rece += match.away_team_goal

    return home_goal_done/len(matches), home_goal_rece/len(matches), \
           home_goal_rece/len(matches), home_goal_done/len(matches)
