import src.util.util as util
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli
import src.application.Domain.Match as Match
import src.util.MLUtil as MLUtil
import src.application.MachineLearning.prediction_accuracy.Predictor as Predictor


def run_experiment_0(exp, league, type_evaluation, **params):

    predictor = Predictor.get_predictor()

    for season in league.get_seasons()[6:]:

        invest = 0
        profit = 0
        accuracy = 0

        print(season)
        if season == util.get_current_season():
            break

        for stage in range(1, league.get_stages_by_season(season)+1):

            # KEY: match id     VALUE: <prediction, probability>
            stage_predictions = predictor.predict(league, season, stage, **params)

            for match_id, pair in stage_predictions.items():
                if len(pair) == 0:
                    continue
                match = Match.read_by_match_id(match_id)
                if util.is_None(match.B365H) or util.is_None(match.B365D) or util.is_None(match.B365A):
                    continue

                predicted_label = pair[0]
                prob = pair[1]
                label = MLUtil.get_label(match)
                m_accuracy, m_invest, m_profit = evaluate_bet(predictor, type_evaluation, label, match, predicted_label, prob)
                accuracy += m_accuracy
                invest += m_invest
                profit += m_profit

            print(stage,"\t",str(round(profit-invest,2)).replace(".",","))
        print("Final investment:\t",invest)
        print("Final profit:\t", profit)


def evaluate_bet(predictor, type_evaluation, label, match, predicted_label, prob):

    if type_evaluation == 1:
        profit = 0
        accuracy = 0
        if label == predicted_label:
            accuracy = 1
            if label == 1:
                profit = match.B365H
            elif label == 0:
                profit = match.B365D
            else:
                profit = match.B365A
        return accuracy, 1, profit

    elif type_evaluation == 2:
        if (predicted_label == 1 and prob < 1/match.B365H) \
            or (predicted_label == 0 and prob < 1 / match.B365D) \
                or (predicted_label == 2 and prob < 1 / match.B365A):
            return 0, 0, 0

        profit = 0
        accuracy = 0
        if label == predicted_label:
            accuracy = 1
            if label == 1:
                profit = match.B365H
            elif label == 0:
                profit = match.B365D
            else:
                profit = match.B365A
        return accuracy, 1, profit

    elif type_evaluation == 3:

        best_predicted_teams = predictor.get_best_team_predicted(match.get_league(), match.season, match.stage)

        if (predicted_label == 1 and prob < 1/match.B365H) \
            or (predicted_label == 0 and prob < 1 / match.B365D) \
                or (predicted_label == 2 and prob < 1 / match.B365A):
            return 0, 0, 0

        profit = 0
        accuracy = 0
        if label == predicted_label:
            accuracy = 1
            if label == 1:
                profit = match.B365H
            elif label == 0:
                profit = match.B365D
            else:
                profit = match.B365A
        return accuracy, 1, profit
