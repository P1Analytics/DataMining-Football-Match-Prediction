import src.util.util as util
import src.application.MachineLearning.experiment.experiment as experiment
from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy


def run_experiment_1(exp, league, ml_train_input_id, ml_train_input_representation, **params):
    print("Running experiment 1")
    print("\tml_train_input_id:", ml_train_input_id)
    print("\tml_train_input_representation:", ml_train_input_representation)

    params["ml_train_input_id"] = ml_train_input_id
    params["ml_train_input_representation"] = ml_train_input_representation

    ml_train_stages_to_train = [10, 25, 50, 95, 130]

    average_time = dict()
    average_accuracy = dict()
    match_predicted = dict()
    for only_team_history in [True, False]:
        for n_matches in ml_train_stages_to_train:
            params["ml_train_stages_to_train"] = n_matches

            curr_denominator = 0
            curr_execution_time = 0
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

                curr_denominator += pa.get_match_predicted()
                curr_execution_time += pa.get_match_predicted() * pa.get_execution_time()
                curr_average_accuracy += pa.get_match_predicted() * pa.get_average_accuracy()

            if curr_denominator != 0:
                average_time[n_matches] = curr_execution_time / curr_denominator
                average_accuracy[n_matches] = curr_average_accuracy / curr_denominator
                match_predicted[n_matches] = curr_denominator

        x, y = experiment.get_x_y(ml_train_stages_to_train, average_accuracy)
        file_name = experiment.get_file_name([ml_train_input_id, ml_train_input_representation, only_team_history],
                                  post="accurcacy")
        exp.create_plot(x, y, file_name, **params)

        x, y = experiment.get_x_y(ml_train_stages_to_train, average_time)
        file_name = experiment.get_file_name([ml_train_input_id, ml_train_input_representation, only_team_history], post="runtime")
        exp.create_plot(x, y, file_name, is_accuracy=False, **params)
