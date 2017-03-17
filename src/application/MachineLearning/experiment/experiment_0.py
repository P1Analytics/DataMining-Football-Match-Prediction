import src.util.util as util
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli
import src.application.Domain.Match as Match
import src.util.MLUtil as MLUtil


def run_experiment_0(exp, league, **params):

    for season in league.get_seasons()[4:]:

        invest = 0
        profit = 0
        accuracy = 0

        print(season)
        if season == util.get_current_season():
            break

        for stage in range(1, league.get_stages_by_season()+1):
            predicted_labels, probability_events, matches_to_predict_id = predict(league, season, stage, **params)

            for match_id, predicted_label, prob in zip(matches_to_predict_id, predicted_labels, probability_events):
                match = Match.read_by_match_id(match_id)
                if util.is_None(match.B365H) or util.is_None(match.B365D) or util.is_None(match.B365A):
                    continue

                label = MLUtil.get_label(match)

                invest += 1
                if label == predicted_label:
                    accuracy += 1
                    if label == 1:
                        profit += 1 * match.B365H
                    elif label == 0:
                        profit += 1 * match.B365D
                    else:
                        profit += 1 * match.B365A

            print(stage,"\t",str(round(profit-invest,2)).replace(".",","))


def predict(league, season, stage, **params):
    ml_alg_method = util.get_default(params, "ml_alg_method", "SVM")
    ml_alg_framework = util.get_default(params, "ml_alg_framework", "my_poisson")
    ml_train_input_id = util.get_default(params, "ml_train_input_id", 5)
    ml_train_input_representation = util.get_default(params, "ml_train_input_representation", 2)
    ml_train_stages_to_train = util.get_default(params, "ml_train_stages_to_train", 10)

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
    except Exception as e:
        print(e)
        return [],[],[]