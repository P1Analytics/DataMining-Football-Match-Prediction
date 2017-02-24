from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy
import src.application.Domain.League as League

def doTest():
    params = dict()
    params["representation"] = 3
    params["season"] = '2015/2016'
    params["ml_train_input_id"] = 2
    italy_league = League.read_by_name("Italy", like=True)[0]
    pa = PredictionAccuracy(italy_league, only_team_history =True, **params)
    pa.get_prediction_accuracy()

doTest()

