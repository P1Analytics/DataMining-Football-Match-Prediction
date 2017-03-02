import src.application.Domain.League as League
from src.application.MachineLearning.experiment.experiment import Experiment

import src.util.util as util
util.init_logger()

def do_test_1():
    italy_league = League.read_by_name("Italy", like=True)[0]
    for mtii in [1, 2, 3]:
        for mtir in [1,2,3,4]:
            if mtii == 1 and (mtir == 1 or mtir == 2):
                continue
            params = {"ml_train_input_id": mtii, "ml_train_input_representation": mtir}
            exp = Experiment(1)
            exp.run(italy_league, complete=False, **params)


def doTest():
    italy_league = League.read_by_name("Italy", like=True)[0]
    exp = Experiment(4)
    params = {"ml_alg_method":"AdaBoostClassifier", "ml_alg_framework":"Sklearn", "ml_train_stages_to_train":10,
              "ml_train_input_id":4}
    exp.run(italy_league, complete=False, **params)


# doTest()
# do_test_1()

def get_average_goals(league, season, stage):
    matches = league.get_training_matches(season, stage, 20)
    home_goal_done = 0          # equals to away_goal_receive
    home_goal_received = 0      # equals to away_goal_done
    for match in matches:
        home_goal_done += match.home_team_goal
        home_goal_received += match.away_team_goal

    return home_goal_done/len(matches), home_goal_received/len(matches), home_goal_received/len(matches), home_goal_done/len(matches)


def get_strength(team, league, season, stage, home=True):
    hgd, hgr, agd, agr = get_average_goals(league, season, stage)
    if home:
        gd, gr, n = team.get_goals_by_train_matches(season, stage, 20, home=home)
        return (gd / n) / hgd, (gr / n) / hgr
    else:
        gd, gr, n = team.get_goals_by_train_matches(season, stage, 20, home=home)
        return (gd / n) / agd, (gr / n) / agr


def get_goal_expectancy(t1_attack_strength, t2_defense_strength, average_t1_goals):
    return t1_attack_strength*t2_defense_strength*average_t1_goals


def get_probability(poisson_list):
    res = dict()
    count = 0
    for elem in poisson_list:
        count += 1
        try:
            res[elem] += 1
        except KeyError:
            res[elem] = 1

    return {k:v/count for k,v in res.items()}


def get_event_probability(g1_prob, g2_prob):
    prob_1 = 0
    prob_X = 0
    prob_2 = 0
    for hg, phg in g1_prob.items():
        for ag, pag in g2_prob.items():
            if hg > ag:
                prob_1 += phg*pag
            elif hg < ag:
                prob_2 += phg*pag
            else:
                prob_X += phg * pag

    return prob_1, prob_X, prob_2

def get_label(match):
    if match.home_team_goal > match.away_team_goal:
        return 1
    elif match.home_team_goal < match.away_team_goal:
        return 2
    else:
        return 0


def predict(event_prob):
    label = 1
    p_max = event_prob[0]
    if p_max < event_prob[1]:
        p_max = event_prob[1]
        label = 0
    if p_max < event_prob[2]:
        p_max = event_prob[2]
        label = 2
    return label, p_max

from numpy.random import poisson
italy_league = League.read_by_name("Italy", like=True)[0]
accuracy = 0
not_accuracy = 0
n1_test = 0
n2_test = 0
for season in italy_league.get_seasons():
    print(season)
    for match in italy_league.get_matches(season=season):
        if season==util.get_current_season() and match.stage>24:
            break
        try:
            hgd, hgr, agd, agr = get_average_goals(italy_league, season, match.stage)
            hgds, hgrs = get_strength(match.get_home_team(), italy_league, season, match.stage, home=True)
            agds, agrs = get_strength(match.get_away_team(), italy_league, season, match.stage, home=False)
            home_exp_goals = get_goal_expectancy(hgds, agrs, hgd)
            away_exp_goals = get_goal_expectancy(agds, hgrs, agd)
            hp = poisson(home_exp_goals, 10000)
            ap = poisson(away_exp_goals, 10000)
            print("hp",get_probability(hp))
            print("ap",get_probability(ap))
            print(get_event_probability(get_probability(hp), get_probability(ap)))
            print(match.stage, match.get_home_team().team_long_name, "vs", match.get_away_team().team_long_name)
            #rprint(hgds, hgrs, "vs", agds, agrs)
            print(home_exp_goals,":",away_exp_goals,"[",match.home_team_goal,":",match.away_team_goal,"]")

            label = get_label(match)
            predict_label, prob = predict(get_event_probability(get_probability(hp), get_probability(ap)))

            if prob < 0.51:
                continue

            print(label, predict_label)
            if label == predict_label:
                accuracy += prob
                n1_test += 1
            else:
                not_accuracy += prob
                n2_test += 1

            print()
        except:
            pass

print(accuracy/n1_test, not_accuracy/n2_test)
