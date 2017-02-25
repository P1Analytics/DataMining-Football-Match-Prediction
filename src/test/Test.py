from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy
import src.application.Domain.League as League

def doTest():
    params = dict()
    params["season"] = '2016/2017'
    params["ml_train_input_id"] = 2
    params["ml_train_stages_to_train"] = 1
    params["ml_train_input_representation"] = 3
    italy_league = League.read_by_name("Italy", like=True)[0]

    for season in italy_league.get_seasons():
        params["season"] = season
        pa = PredictionAccuracy(italy_league, only_team_history=False, **params)
        pa.get_prediction_accuracy()

        print("Average accuracy", pa.get_average_accuracy())
        print("Match predicted", pa.get_match_predicted())

doTest()

