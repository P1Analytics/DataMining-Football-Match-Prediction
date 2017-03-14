import src.util.util as util
import src.application.MachineLearning.experiment.experiment as experiment
from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli
import src.application.Domain.Match as Match
import src.util.MLUtil as MLUtil


def run_experiment_0(exp, league, **params):

    invest = 0
    profit = 0
    for season in league.get_seasons()[1:]:
        if season == util.get_current_season():
            break

        for stage in range(1, 39):
            predicted_labels, probability_events, matches_to_predict_id = predict(league, season, stage, **params)

            for match_id, predicted_label, prob in zip(matches_to_predict_id, predicted_labels, probability_events):

                match = Match.read_by_match_id(match_id)
                if util.is_None(match.B365H) or util.is_None(match.B365D) or util.is_None(match.B365A):
                    continue

                label = MLUtil.get_label(match)

                min_bet_odds = 1 / prob
                if predicted_label == 1 and min_bet_odds > match.B365H:
                    continue
                if predicted_label == 2 and min_bet_odds > match.B365A:
                    continue
                if predicted_label == 0 and min_bet_odds > match.B365D:
                    continue

                sum_to_invest = 1
                if prob > 0.90:
                    sum_to_invest = 1
                elif prob > 0.8:
                    sum_to_invest = 1
                elif prob > 0.7:
                    sum_to_invest = 1
                #print(match.get_home_team().team_long_name, "vs", match.get_away_team().team_long_name, predicted_label, label)
                invest += sum_to_invest
                if label == predicted_label:
                    if label == 1:
                        profit += sum_to_invest*match.B365H
                    elif label == 0:
                        profit += sum_to_invest*match.B365D
                    else:
                        profit += sum_to_invest*match.B365A

            print(stage, invest, profit)
            print()


def predict(league, season, stage, **params):
    ml_alg_method = util.get_default(params, "ml_alg_method", "SVM")
    ml_alg_framework = util.get_default(params, "ml_alg_framework", "my_poisson")
    ml_train_input_id = util.get_default(params, "ml_train_input_id", 5)
    ml_train_input_representation = util.get_default(params, "ml_train_input_representation", 1)
    ml_train_stages_to_train = util.get_default(params, "ml_train_stages_to_train", 20)

    try:
        matches, labels, matches_id, matches_to_predict, matches_to_predict_id, labels_to_predict = \
            mli.get_input_to_train(ml_train_input_id,
                                   league,
                                   ml_train_input_representation,
                                   stage,
                                   ml_train_stages_to_train,
                                   season)

        ml_alg = mla.get_machine_learning_algorithm(ml_alg_framework,
                                                    ml_alg_method,
                                                    matches,
                                                    labels,
                                                    matches_id,
                                                    train_percentage=1,
                                                    )

        ml_alg.train()
        predicted_labels, probability_events = ml_alg.predict(matches_to_predict)
        return predicted_labels, probability_events, matches_to_predict_id
    except:
        return [],[],[]