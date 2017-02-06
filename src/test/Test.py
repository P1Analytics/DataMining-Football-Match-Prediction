import src.application.MachineLearning.MachineLearningInput as MLInput
import src.application.MachineLearning.MachineLearningAlgorithm as MachineLearningAlgorithm


def doTest():
    #matches, labels, matches_names = MLInput.get_datas_by_league("Italy Serie A", "2015/2016")
    matches, labels, matches_names = MLInput.team_home_away_form("Italy Serie A", 4, n=9, season= "2015/2016")
    params = {"batch_size": 500, "number_step":1000, "kernel":"linear"}
    MachineLearningAlgorithm.run_all_algorithms(matches, labels, matches_names, **params)

doTest()


