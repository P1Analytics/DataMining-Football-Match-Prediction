import src.application.MachineLearning.MachineLearningInput as MLInput
import src.application.MachineLearning.MachineLearningAlgorithm as MachineLearningAlgorithm
import src.util.util as util

import numpy as np
from src.application.Exception.MLException import MLException


def get_prediction_accuracy(league, only_team_history=False, **params):

    season = util.get_default(params, "season", util.get_current_season())
    stages = util.get_default(params, "stages", [s for s in range(1, 39)])
    representation = util.get_default(params, "representation", 1)

    ml_train_stages_to_train = util.get_default(params, "ml_train_stages_to_train", 10)
    ml_train_input_id = util.get_default(params, "ml_train_input_id", 1)

    ml_alg_framework = util.get_default(params, "ml_alg_framework", "Sklearn")
    ml_alg_method = util.get_default(params, "ml_alg_method", "SVM")

    ml_alg_params = dict()
    ml_alg_params["number_step"] = util.get_default(params, "ml_alg_number_step", 1000)
    ml_alg_params["kernel"] = util.get_default(params, "ml_alg_kernel", "rbf")
    ml_alg_params["k"] = util.get_default(params, "ml_alg_k", 9)

    print("Season:", season)
    print("Stages:", stages)
    print("ml_train_stages_to_train", ml_train_stages_to_train)
    print("ml_train_input_id", ml_train_input_id)
    print("only_team_history", only_team_history)

    accuracy_stage = dict()
    for stage in stages:
        print(accuracy_stage)
        print()
        print(season, stage)
        print()

        if only_team_history:
            # train ml algorithm only with past mathces of teams
            for match in league.get_matches(season=season, stage=stage):
                home_team = match.get_home_team()
                away_team = match.get_away_team()
                try:
                    home_matches, home_labels, home_matches_names, home_matches_to_predict, \
                    home_matches_to_predict_names, home_labels_to_preidct = \
                        MLInput.get_input_to_train(ml_train_input_id,
                                                   home_team,
                                                   representation,
                                                   stage,
                                                   stages_to_train=ml_train_stages_to_train,
                                                   season=season)

                    away_matches, away_labels, away_matches_names, away_matches_to_predict, \
                    away_matches_to_predict_names, away_labels_to_preidct = \
                        MLInput.get_input_to_train(ml_train_input_id,
                                                   away_team,
                                                   representation,
                                                   stage,
                                                   stages_to_train=ml_train_stages_to_train,
                                                   season=season)

                    matches = np.concatenate((home_matches, away_matches), axis=0)
                    labels = np.concatenate((home_labels, away_labels), axis=0)
                    matches_names = home_matches_names.extend(away_matches_names)
                except MLException as mle:
                    print()
                    print(mle, home_team.team_long_name, away_team.team_long_name)
                    print()
                    continue

                train_predict(labels, home_labels_to_preidct, matches, matches_names, home_matches_to_predict,
                              home_matches_to_predict_names, ml_alg_framework, ml_alg_method, ml_alg_params,
                              accuracy_stage)
        else:
            # train ml algorithm with all league matches
            try:
                matches, labels, matches_names, matches_to_predict, matches_to_predict_names, \
                labels_to_preidct = MLInput.get_input_to_train(ml_train_input_id,
                                                               league,
                                                               representation,
                                                               stage,
                                                               stages_to_train=ml_train_stages_to_train,
                                                               season=season)
            except MLException as mle:
                print(mle)
                continue

            train_predict(labels, labels_to_preidct, matches, matches_names, matches_to_predict,
                          matches_to_predict_names, ml_alg_framework, ml_alg_method, ml_alg_params,
                          accuracy_stage)


def train_predict(labels, labels_to_predict, matches, matches_names, matches_to_predict, matches_to_predict_names,
                  ml_alg_framework, ml_alg_method, ml_alg_params, accuracy_stage_dic):
    ml_alg = MachineLearningAlgorithm.get_machine_learning_algorithm(ml_alg_framework,
                                                                     ml_alg_method,
                                                                     matches,
                                                                     labels,
                                                                     data_description=matches_names,
                                                                     train_percentage=1,
                                                                     **ml_alg_params)
    ml_alg.train()
    predicted_labels, probability_events = ml_alg.predict(matches_to_predict)
    accuracy = 0
    team_accuracy_dic = {}
    for p, l, s in zip(predicted_labels, labels_to_predict, matches_to_predict_names):
        print("*****")
        print(s)
        s = s.split("vs")
        print('\tResult:', l, "\tPredicted", p)
        print("*****")
        if p == l:
            accuracy += 1
            team_accuracy_dic[s[0].strip()] = [accuracy, 1]
            team_accuracy_dic[s[1].strip()] = [accuracy, 1]
        else:
            team_accuracy_dic[s[0].strip()] = [accuracy, 1]
            team_accuracy_dic[s[1].strip()] = [accuracy, 1]

    update_team_accuracy(accuracy_stage_dic, team_accuracy_dic)


def update_team_accuracy(team_accuracy_dic, stage_accuracy_dic):
    for k,v in stage_accuracy_dic.items():
        try:
            accuracy  = team_accuracy_dic[k][0] + v[0]
            predicted_game = team_accuracy_dic[k][1] + v[1]
            team_accuracy_dic[k] = [accuracy,predicted_game]
        except KeyError:
            team_accuracy_dic[k] = v

    return team_accuracy_dic


'''
fig = plt.figure()
        plt.title(italy_league.name+" ["+season+"]")
        #plt.plot(average_accuracy[1][1], label='r1')
        #plt.plot(average_accuracy[2][1], label='r2')
        #plt.plot(average_accuracy[3][1], label='r3')
        #plt.plot(average_accuracy[4][1], label='r4')
        plt.plot(range(stage-len(dict_to_plot[1]), stage), dict_to_plot[1], marker='o', linestyle='-', label='r1, '+str(round(average_accuracy[1][1]/average_accuracy[1][0],2)))
        #plt.plot(range(stage-len(dict_to_plot[1]), stage), dict_to_plot[2], marker='o', linestyle='-', label='r2, '+str(round(average_accuracy[2][1]/average_accuracy[2][0],2)))
        #plt.plot(range(stage-len(dict_to_plot[1]), stage), dict_to_plot[3], marker='o', linestyle='-', label='r3, '+str(round(average_accuracy[3][1]/average_accuracy[3][0],2)))
        #plt.plot(range(stage-len(dict_to_plot[1]), stage), dict_to_plot[4], marker='o', linestyle='-', label='r4, '+str(round(average_accuracy[4][1]/average_accuracy[4][0],2)))

        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        fig.savefig(util.get_project_directory()+"data/figure/fig_"+season.replace('/','_')+"_"+str(stage)+".png", bbox_inches='tight')
        plt.close()'''
