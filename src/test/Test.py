import src.application.MachineLearning.MachineLearningInput as MLInput
import src.application.MachineLearning.MachineLearningAlgorithm as MachineLearningAlgorithm
from bs4 import BeautifulSoup
import src.application.Domain.League as League
import src.application.Domain.Shot as Shot


def doTest():
    matches, labels, matches_names = MLInput.get_datas_by_league("Italy Serie A", "2015/2016")
    #matches, labels, matches_names = MLInput.team_form("Italy Serie A", 4, n=None, season="2015/2016")
    #matches, labels, matches_names = MLInput.team_home_away_form("Italy Serie A", 4, n=None, season= "2015/2016")
    #matches, labels, matches_names = MLInput.match_statistics("Italy Serie A", n=None, season="2015/2016")
    params = {"batch_size": 259, "number_step":1000, "kernel":"rbf", "k":9}
    MachineLearningAlgorithm.run_all_algorithms(matches, labels, matches_names, **params)


doTest()


