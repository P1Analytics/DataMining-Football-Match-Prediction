import logging
import time

import src.application.MachineLearning.MachineLearningInput as MLInput
import src.application.MachineLearning.MachineLearningAlgorithm as MachineLearningAlgorithm
import src.util.util as util

import numpy as np
from src.application.Exception.MLException import MLException


log = logging.getLogger(__name__)


class TeamPredictionAccuracy(object):

    def __init__(self, team):
        self.team = team
        self.n_succesfull_predicted_label = 0
        self.n_predicted_game = 0

    def next_prediction(self, prediction, label):
        if prediction == label:
            self.n_succesfull_predicted_label += 1

        self.n_predicted_game += 1

    def __str__(self):
        return "<"+self.team+", "+str(self.n_succesfull_predicted_label)+"/"+str(self.n_predicted_game)+">"


class PredictionAccuracy(object):

    def __init__(self, league, only_team_history=False, **params):
        self.league = league
        self.only_team_history = only_team_history

        self.season = util.get_default(params, "season", util.get_current_season())
        self.stages = util.get_default(params, "stages", [s for s in range(1, 39)])

        self.ml_alg_method    = util.get_default(params, "ml_alg_method", "SVM")
        self.ml_alg_framework = util.get_default(params, "ml_alg_framework", "Sklearn")

        self.ml_train_input_id        = util.get_default(params, "ml_train_input_id", 1)
        self.representation           = util.get_default(params, "ml_train_input_representation", 1)
        self.ml_train_stages_to_train = util.get_default(params, "ml_train_stages_to_train", 10)

        self.ml_alg_params = dict()
        self.ml_alg_params["k"]           = util.get_default(params, "ml_alg_k", 9)
        self.ml_alg_params["kernel"]      = util.get_default(params, "ml_alg_kernel", "rbf")
        self.ml_alg_params["number_step"] = util.get_default(params, "ml_alg_number_step", 1000)

        self.n_predicted_match     = 0
        self.accuracy_by_team_dic  = dict()
        self.accuracy_by_stage_dic = {x: 0 for x in self.stages}

        self.finish_time = -1

        log.debug("[" + self.season + "], size train [" + str(self.ml_train_stages_to_train) + "], train input id[" +
                  str(self.ml_train_input_id) + "], consider only team history [" + str(self.only_team_history) + "]")
        print("[" + self.season + "], size train [" + str(self.ml_train_stages_to_train) + "], train input id[" +
                  str(self.ml_train_input_id) + "], consider only team history [" + str(self.only_team_history) + "],"
                  " ml_alg_framework ["+self.ml_alg_framework+"], ml_alg_method ["+self.ml_alg_method+"]")

    def get_average_accuracy(self):
        if len(self.accuracy_by_stage_dic) == 0:
            return -1
        avg_accuracy = 0
        for stage, accuracy in self.accuracy_by_stage_dic.items():
            avg_accuracy += accuracy
        return avg_accuracy / len(self.accuracy_by_stage_dic)

    def get_match_predicted(self):
        return self.n_predicted_match

    def get_stages_accuracy(self):
        return self.accuracy_by_stage_dic

    def print_statistcis(self):
        print(self.accuracy_by_stage_dic)
        print([p.__str__() for t, p in self.accuracy_by_team_dic.items()])

    def get_execution_time(self):
        return self.finish_time

    def compute_prediction_accuracy(self):
        start_time = time.time()
        for stage in self.stages:
            if self.only_team_history:
                # train ml algorithm only with past mathces of teams
                n_predicted_match = 0
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

                        accuracy = self.train_predict(stage)
                        self.accuracy_by_stage_dic[stage] += accuracy
                        n_predicted_match += 1
                    except MLException as mle:
                        #log.debug(mle, home_team.team_long_name, away_team.team_long_name)
                        continue

                if n_predicted_match != 0:
                    self.accuracy_by_stage_dic[stage] = self.accuracy_by_stage_dic[stage]/n_predicted_match
                    self.n_predicted_match += n_predicted_match
                else:
                    del(self.accuracy_by_stage_dic[stage])

            else:
                # train ml algorithm with all league matches
                try:

                    self.matches, \
                        self.labels, \
                        self.matches_names, \
                        self.matches_to_predict, \
                        self.matches_to_predict_names, \
                        self.labels_to_predict = MLInput.get_input_to_train(self.ml_train_input_id,
                                                                            self.league,
                                                                            self.representation,
                                                                            stage,
                                                                            stages_to_train=self.ml_train_stages_to_train,
                                                                            season=self.season)
                    accuracy = self.train_predict(stage)

                    self.accuracy_by_stage_dic[stage] = accuracy
                    self.n_predicted_match += len(self.labels_to_predict)

                except MLException as mle:
                    del(self.accuracy_by_stage_dic[stage])
                    log.debug(mle)
                    continue
        self.finish_time = time.time() - start_time

    def train_predict(self, stage):
        ml_alg = MachineLearningAlgorithm.get_machine_learning_algorithm(self.ml_alg_framework,
                                                                         self.ml_alg_method,
                                                                         self.matches,
                                                                         self.labels,
                                                                         data_description=self.matches_names,
                                                                         train_percentage=1,
                                                                         **self.ml_alg_params)
        try:
            ml_alg.train()
        except ValueError as ve:
            print(ve)
            raise MLException(3)

        predicted_labels, probability_events = ml_alg.predict(self.matches_to_predict)
        accuracy = 0
        print("***",stage,"***")
        for predicted_label, prob, label, match_name in zip(predicted_labels,
                                                            probability_events,
                                                            self.labels_to_predict,
                                                            self.matches_to_predict_names):

            print(match_name, predicted_label, "[",label,"]")

            if predicted_label == label:
                accuracy += 1
            home_team_name = match_name.split("vs")[0].strip()
            away_team_name = match_name.split("vs")[1].strip()
            try:
                self.accuracy_by_team_dic[home_team_name].next_prediction(predicted_label, label)
            except KeyError:
                self.accuracy_by_team_dic[home_team_name] = TeamPredictionAccuracy(home_team_name)
                self.accuracy_by_team_dic[home_team_name].next_prediction(predicted_label, label)
            try:
                self.accuracy_by_team_dic[away_team_name].next_prediction(predicted_label, label)
            except KeyError:
                self.accuracy_by_team_dic[away_team_name] = TeamPredictionAccuracy(away_team_name)
                self.accuracy_by_team_dic[away_team_name].next_prediction(predicted_label, label)

        return accuracy/len(predicted_labels)
