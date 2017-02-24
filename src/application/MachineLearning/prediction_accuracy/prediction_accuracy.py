import src.application.MachineLearning.MachineLearningInput as MLInput
import src.application.MachineLearning.MachineLearningAlgorithm as MachineLearningAlgorithm
import src.util.util as util

import numpy as np
from src.application.Exception.MLException import MLException


class PredictionAccuracy(object):
    def __init__(self,league, only_team_history=False, **params):
        self.league = league
        self.only_team_history = only_team_history

        self.season = util.get_default(params, "season", util.get_current_season())
        self.stages = util.get_default(params, "stages", [s for s in range(1, 39)])
        self.representation = util.get_default(params, "representation", 1)

        self.ml_train_stages_to_train = util.get_default(params, "ml_train_stages_to_train", 10)
        self.ml_train_input_id = util.get_default(params, "ml_train_input_id", 1)

        self.ml_alg_framework = util.get_default(params, "ml_alg_framework", "Sklearn")
        self.ml_alg_method = util.get_default(params, "ml_alg_method", "SVM")

        self.ml_alg_params = dict()
        self.ml_alg_params["number_step"] = util.get_default(params, "ml_alg_number_step", 1000)
        self.ml_alg_params["kernel"] = util.get_default(params, "ml_alg_kernel", "rbf")
        self.ml_alg_params["k"] = util.get_default(params, "ml_alg_k", 9)

        self.accuracy_stage_dic = dict()

        print("Season:", self.season)
        print("Stages:", self.stages)
        print("ml_train_stages_to_train", self.ml_train_stages_to_train)
        print("ml_train_input_id", self.ml_train_input_id)
        print("only_team_history", self.only_team_history)

    def get_prediction_accuracy(self):
        for stage in self.stages:
            print(self.accuracy_stage_dic)
            print()
            print(self.season, stage)
            print()

            if self.only_team_history:
                # train ml algorithm only with past mathces of teams
                for match in self.league.get_matches(season=self.season, stage=stage):
                    home_team = match.get_home_team()
                    away_team = match.get_away_team()
                    try:
                        home_matches, \
                        home_labels, \
                        home_matches_names, \
                        home_matches_to_predict, \
                        home_matches_to_predict_names, \
                        home_labels_to_predict = \
                            MLInput.get_input_to_train(self.ml_train_input_id,
                                                       home_team,
                                                       self.representation,
                                                       stage,
                                                       stages_to_train=self.ml_train_stages_to_train,
                                                       season=self.season)

                        away_matches, away_labels, away_matches_names, away_matches_to_predict, \
                        away_matches_to_predict_names, away_labels_to_preidct = \
                            MLInput.get_input_to_train(self.ml_train_input_id,
                                                       away_team,
                                                       self.representation,
                                                       stage,
                                                       stages_to_train=self.ml_train_stages_to_train,
                                                       season=self.season)

                        self.matches = np.concatenate((home_matches, away_matches), axis=0)
                        self.labels = np.concatenate((home_labels, away_labels), axis=0)
                        self.matches_names = home_matches_names.extend(away_matches_names)
                        self.matches_to_predict = home_matches_to_predict               # the same works with away
                        self.matches_to_predict_names = home_matches_to_predict_names   # the same works with away
                        self.labels_to_predict = home_labels_to_predict                 # the same works with away
                    except MLException as mle:
                        print()
                        print(mle, home_team.team_long_name, away_team.team_long_name)
                        print()
                        continue

                    self.train_predict()
            else:
                # train ml algorithm with all league matches
                try:
                    self.matches, \
                    self.labels, \
                    self.matches_names, \
                    self.matches_to_predict, \
                    self.matches_to_predict_names, \
                    self.labels_to_preidct = MLInput.get_input_to_train(self.ml_train_input_id,
                                                                   self.league,
                                                                   self.representation,
                                                                   stage,
                                                                   stages_to_train=self.ml_train_stages_to_train,
                                                                   season=self.season)
                except MLException as mle:
                    print(mle)
                    continue

                self.train_predict()

    def train_predict(self):
        ml_alg = MachineLearningAlgorithm.get_machine_learning_algorithm(self.ml_alg_framework,
                                                                         self.ml_alg_method,
                                                                         self.matches,
                                                                         self.labels,
                                                                         data_description=self.matches_names,
                                                                         train_percentage=1,
                                                                         **self.ml_alg_params)
        ml_alg.train()
        predicted_labels, probability_events = ml_alg.predict(self.matches_to_predict)
        accuracy = 0
        team_accuracy_dic = {}
        for p, l, s in zip(predicted_labels, self.labels_to_predict, self.matches_to_predict_names):
            print("*****")
            print(s)
            s = s.split("vs")
            print('\tResult:', l, "\tPredicted", p)
            print("*****")
            if p == l:
                accuracy += 1
            team_accuracy_dic[s[0].strip()] = [accuracy, 1]
            team_accuracy_dic[s[1].strip()] = [accuracy, 1]

        update_team_accuracy(self.accuracy_stage_dic, team_accuracy_dic)


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
