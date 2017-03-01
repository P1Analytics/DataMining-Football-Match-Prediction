import src.util.util as util
import src.application.MachineLearning.experiment.experiment as experiment
import src.application.MachineLearning.MachineLearningAlgorithm as mla
from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy


def run_experiment_3(exp, league, ml_train_input_id, ml_train_input_representation, ml_train_stages_to_train):
    params = dict()

    #frameworks = mla.get_frameworks()
    frameworks = ["Sklearn"]
    methods = mla.get_methods()

    average_time = {f:{m:0 for m in methods} for f in frameworks}
    average_accuracy = {f:{m:0 for m in methods} for f in frameworks}
    match_predicted = {f:{m:0 for m in methods} for f in frameworks}

    params["ml_train_input_id"] = ml_train_input_id
    params["ml_train_input_representation"] = ml_train_input_representation
    params["ml_train_stages_to_train"] = ml_train_stages_to_train

    for only_team_history in [True, False]:
        try:
            for ml_alg_framework in frameworks:
                for ml_alg_method in methods:
                    params["ml_alg_method"] = ml_alg_method
                    params["ml_alg_framework"] = ml_alg_framework
                    print(params)
                    curr_denominator = 0
                    curr_execution_time = 0
                    curr_average_accuracy = 0

                    for season in league.get_seasons():
                        if season == util.get_current_season():
                            break

                        print(season, only_team_history, ml_alg_framework, ml_alg_method)

                        params["season"] = season

                        pa = PredictionAccuracy(league, only_team_history=only_team_history, **params)
                        pa.compute_prediction_accuracy()

                        print("Average accuracy:", pa.get_average_accuracy())
                        print("Match predicted:", pa.get_match_predicted())
                        print("Time:", pa.get_execution_time())

                        curr_denominator += pa.get_match_predicted()
                        curr_execution_time += pa.get_match_predicted() * pa.get_execution_time()
                        curr_average_accuracy += pa.get_match_predicted() * pa.get_average_accuracy()
                        break

                    if curr_denominator != 0:
                        average_time[ml_alg_framework][ml_alg_method] = curr_execution_time / curr_denominator
                        average_accuracy[ml_alg_framework][ml_alg_method] = curr_average_accuracy / curr_denominator
                        match_predicted[ml_alg_framework][ml_alg_method] = curr_denominator

                x, y = experiment.get_x_y(average_accuracy[ml_alg_framework].keys(), average_accuracy[ml_alg_framework])
                file_name = experiment.get_file_name([ml_alg_framework, only_team_history],
                                          post="accurcacy")
                exp.create_plot(x, y, file_name, **params)

                x, y = experiment.get_x_y(average_time[ml_alg_framework].keys(), average_time[ml_alg_framework])
                file_name = experiment.get_file_name([ml_alg_framework, only_team_history], post="runtime")
                exp.create_plot(x, y, file_name, is_accuracy=False, **params)
        except AttributeError:
            continue
