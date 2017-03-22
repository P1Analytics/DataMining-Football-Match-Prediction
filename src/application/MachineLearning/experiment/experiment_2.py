import src.util.util as util
import src.application.MachineLearning.experiment.experiment as experiment
from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy
import src.application.MachineLearning.MachineLearningAlgorithm as mla


class entry(object):
    def __init__(self, window):
        self.window = window
        self.accuracies = dict()
        self.times = dict()
        self.match_predicted = dict()

    def add_accuracy(self, framework, method, accuracy, predicted_matches, time):
        if method:
            key = framework+"_"+method
        else:
            key = framework
        try:
            self.match_predicted[key] += predicted_matches
        except KeyError:
            self.match_predicted[key] = predicted_matches

        try:
            self.accuracies[key] += accuracy*predicted_matches
        except KeyError:
            self.accuracies[key] = accuracy*predicted_matches

        try:
            self.times[key] += time
        except KeyError:
            self.times[key] = time

    def __str__(self):
        # window \t number of successful prediction, number of total predictions, execution time
        ret = ""
        for k,v in self.accuracies.items():
            ret += str(self.window)+"\t"\
                   + k +"\t" + str(int(v)) + "\t"+str(self.match_predicted[k])+"\t"+str(int(self.times[k]))+"\t"\
                   + str(round(v/max(self.match_predicted[k],1),3)).replace(".",",")+"\t"\
                   + str(round(self.times[k]/max(self.match_predicted[k],1),3)).replace(".",",")+"\n"

        return ret


def run_experiment_2(exp, league, ml_train_input_id, ml_train_input_representation, **params):
    print("Running experiment 2")
    print("\tml_train_input_id:", ml_train_input_id)
    print("\tml_train_input_representation:", ml_train_input_representation)

    params["ml_train_input_id"] = ml_train_input_id
    params["ml_train_input_representation"] = ml_train_input_representation

    # ml_train_stages_to_train = [9,11,19,35,71,105,141,175,211,245,281]
    # shrink windows
    ml_train_stages_to_train = [9, 11, 19, 35, 71, 105, 141]

    plot_entries = {w:entry(w) for w in ml_train_stages_to_train}

    for n_matches in ml_train_stages_to_train:
        params["ml_train_stages_to_train"] = n_matches

        for season in league.get_seasons()[-3:]:
            # only consider last two season
            if season == util.get_current_season():
                break

            params["season"] = season
            for f in mla.get_frameworks():

                if ml_train_input_id not in mla.get_inputs_by_framework(f):
                    continue

                if len(mla.get_methods_by_framework(f))==0:
                    # framework has no methods (ex. poisson)
                    #   --> just predict without specifying it

                    params["ml_alg_framework"] = f
                    pa = PredictionAccuracy(league, only_team_history=False, **params)
                    pa.compute_prediction_accuracy()
                    plot_entries[n_matches].add_accuracy(f, None, pa.get_average_accuracy(), pa.get_match_predicted(), pa.get_execution_time())

                for m in mla.get_methods_by_framework(f):
                    # framework can be used in different manner (ex. SKlearn)
                    #   --> test every algorithm available (SVM, Knn,..)

                    params["ml_alg_method"]=m
                    params["ml_alg_framework"]=f
                    pa = PredictionAccuracy(league, only_team_history=False, **params)
                    pa.compute_prediction_accuracy()
                    plot_entries[n_matches].add_accuracy(f, m, pa.get_average_accuracy(), pa.get_match_predicted(),
                                                         pa.get_execution_time())

                    print(plot_entries[n_matches])

            report = open(exp.experiment_dir+"/report_"+str(ml_train_input_id)+"_"
                          +str(ml_train_input_representation)+".txt", "w")
            report.write("Input id:\t"+str(ml_train_input_id)+"\n")
            report.write("Representation:\t" + str(ml_train_input_representation) + "\n")
            report.write("Window\tMethod\tSuccessful Pred.\tTotal Pred.\tExecution Time\tAccuracy\tTime x prediction\n")
            sorted(plot_entries)
            for w in sorted(plot_entries.keys()):
                report.write(plot_entries[w].__str__()+"\n")

            report.close()
