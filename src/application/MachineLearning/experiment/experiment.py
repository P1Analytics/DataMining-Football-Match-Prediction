import os
import src.util.util as util
import src.application.MachineLearning.MachineLearningInput as mli
from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy
from src.application.MachineLearning.experiment.experiment_plot import PlotExperiment

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

experiments = {
    0: "check accuracy of each stage by seasons",
    1: "Given in input a match representation, it performs an accuracy assesment that depends on match/league team "
       "history and number of previous stage to consider"
}

class Experiment(object):
    def __init__(self, type):
        self.type = type
        self.id = util.get_id_by_time()+"_"+str(self.type)

        self.experiment_dir = util.get_project_directory()+"data/experiments/"+self.id
        os.makedirs(self.experiment_dir)

    def run(self, league, complete=True, **params):
        if self.type == 1:
            if complete:
                for ml_train_input_id in mli.get_input_ids():
                    for ml_train_input_representation in mli.get_representations(ml_train_input_id):
                        self.run_experiment_1(league, ml_train_input_id, ml_train_input_representation)
            else:
                ml_train_input_id =             util.get_default(params, "ml_train_input_id", 1)
                ml_train_input_representation = util.get_default(params, "ml_train_input_representation", 1)
                self.run_experiment_1(league, ml_train_input_id, ml_train_input_representation)
        else:
            params = dict()
            params["season"] = '2016/2017'
            params["stages"] = [26]
            params["ml_train_input_id"] = 3
            params["ml_train_stages_to_train"] = 10
            params["ml_train_input_representation"] = 3

            for season in league.get_seasons():
                print("Elaboratinfg season..", season)
                params["season"] = season
                pa = PredictionAccuracy(league, only_team_history=False, **params)
                pa.compute_prediction_accuracy()

                print("Average accuracy", pa.get_average_accuracy())
                print("Match predicted", pa.get_match_predicted())

                x = []
                y = []
                for stage, acc in pa.get_stages_accuracy().items():
                    x.append(stage)
                    y.append(acc)
                p = PlotExperiment(self.type, y, x, **params)
                p.plot(path_file=self.experiment_dir+"/"+season.replace("/","_")+".png")

    def run_experiment_1(self, league, ml_train_input_id, ml_train_input_representation):
        params = dict()
        params["ml_train_input_id"] = ml_train_input_id
        params["ml_train_input_representation"] = ml_train_input_representation

        ml_train_stages_to_train = [5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 23, 26, 29, 33, 37, 42, 47, 53, 60, 67, 75,
                                    85, 95, 105, 115, 130, 155, 170, 200, 235, 275]

        average_time     = dict()
        average_accuracy = dict()
        match_predicted  = dict()
        for only_team_history in [True, False]:
            for n_matches in ml_train_stages_to_train:
                params["ml_train_stages_to_train"] = n_matches

                curr_denominator      = 0
                curr_execution_time   = 0
                curr_average_accuracy = 0

                for season in league.get_seasons():
                    if season == util.get_current_season():
                        break

                    print(season, n_matches)

                    params["season"] = season

                    pa = PredictionAccuracy(league, only_team_history=only_team_history, **params)
                    pa.compute_prediction_accuracy()

                    print("Average accuracy:", pa.get_average_accuracy())
                    print("Match predicted:", pa.get_match_predicted())
                    print("Time:", pa.get_execution_time())

                    curr_denominator      += pa.get_match_predicted()
                    curr_execution_time   += pa.get_match_predicted() * pa.get_execution_time()
                    curr_average_accuracy += pa.get_match_predicted() * pa.get_average_accuracy()

                if curr_denominator != 0:
                    average_time[n_matches]     = curr_execution_time   / curr_denominator
                    average_accuracy[n_matches] = curr_average_accuracy / curr_denominator
                    match_predicted[n_matches]  = curr_denominator

            x, y = get_x_y(ml_train_stages_to_train, average_accuracy)
            file_name = get_file_name([ml_train_input_id, ml_train_input_representation, only_team_history], post="accurcacy")
            self.create_plot(x, y, file_name, **params)

            x, y = get_x_y(ml_train_stages_to_train, average_time)
            file_name = get_file_name([ml_train_input_id, ml_train_input_representation, only_team_history], post="runtime")
            self.create_plot(x, y, file_name, is_accuracy=False, **params)

    def create_plot(self, x, y, file_name, is_accuracy=True, **params):
        p = PlotExperiment(self.type, y, x, **params)
        p.plot(path_file=self.experiment_dir + "/" + file_name, is_accuracy=is_accuracy)


def get_x_y(x_list, y_dict):
    x = []
    y = []
    for x_i in x_list:
        try:
            x.append(x_i)
            y.append(y_dict[x_i])
        except KeyError:
            continue
    return x, y


def get_file_name(params, extension="png", pre=None, post=None):
    file_name = ""
    print(pre)
    if pre:
        file_name += pre+"_"

    for p in params:
        file_name += str(p)+"_"

    file_name = file_name[:-1]
    if post:
        file_name += "_"+post

    return file_name+"."+extension
