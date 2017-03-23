import math
import src.util.util as util
import src.application.MachineLearning.experiment.experiment as experiment
import src.application.MachineLearning.MachineLearningAlgorithm as mla
from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy
import src.application.MachineLearning.prediction_accuracy.Predictor as Predictor
import src.application.Domain.Match as Match


def run_experiment_4(exp, league, predictor=Predictor.get_predictor(), **params):

    for season in league.get_seasons()[4: ]:
        distance = {i: 0 for i in [0, 1, 2]}
        number_bet_odds = {i: 0 for i in [0, 1, 2]}
        print(season)
        for stage in range(1, league.get_stages_by_season(season)+1):

            stage_predictions = predictor.predict(league, season, stage, **params)

            for match_id, pair in stage_predictions.items():
                if len(pair) == 0:
                    continue
                match = Match.read_by_match_id(match_id)
                if util.is_None(match.B365H) or util.is_None(match.B365D) or util.is_None(match.B365A)\
                        or match.B365H == 0 or match.B365D == 0 or match.B365A == 0:
                    continue

                predicted_label, prob = pair[0], pair[1]

                our_bet_odds = 1 / prob
                bm_bet_odds = -1

                if predicted_label == 1:
                    bm_bet_odds = match.B365H
                elif predicted_label == 0:
                    bm_bet_odds = match.B365D
                elif predicted_label == 2:
                    bm_bet_odds = match.B365A

                distance[predicted_label] += math.fabs(our_bet_odds - bm_bet_odds)
                number_bet_odds[predicted_label] += 1

        print(1, distance[1] / max(number_bet_odds[1],1))
        print(0, distance[0] / max(number_bet_odds[0],1))
        print(2, distance[2] / max(number_bet_odds[2],1))

