import src.application.MachineLearning.prediction_accuracy.prediction_accuracy as pa
import src.application.Domain.League as League

def doTest():
    params = dict()
    params["representation"] = 3
    params["ml_train_input_id"] = 2
    italy_league = League.read_by_name("Italy", like=True)[0]
    pa.get_prediction_accuracy(italy_league, only_team_history =True, **params)

doTest()

