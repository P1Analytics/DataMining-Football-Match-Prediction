import os
import src.util.util as util

from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy
from src.application.MachineLearning.experiment.experiment_plot import PlotExperiment


experiments = {
    0: "check accuracy of each stage by seasons"
}

class Experiment(object):
    def __init__(self, type):
        self.type = type
        self.id = util.get_id_by_time()

        self.experiment_dir = util.get_project_directory()+"data/experiments/"+self.id
        os.makedirs(self.experiment_dir)


    def run(self, league):
        params = dict()
        #params["season"] = '2016/2017'
        #params["stages"] = [35,36,37,38]
        params["ml_train_input_id"] = 1
        params["ml_train_stages_to_train"] = 10
        params["ml_train_input_representation"] = 3

        for season in league.get_seasons():
            print("Elaboratinfg season..", season)
            params["season"] = season
            pa = PredictionAccuracy(league, only_team_history=False, **params)
            pa.get_prediction_accuracy()

            print("Average accuracy", pa.get_average_accuracy())
            print("Match predicted", pa.get_match_predicted())

            x = []
            y = []
            for stage, acc in pa.get_stages_accuracy().items():
                x.append(stage)
                y.append(acc)
            p = PlotExperiment(self.type, y, x, **params)
            p.plot(path_file=self.experiment_dir+"/"+season.replace("/","_")+".png")