import src.application.Domain.League as League
from src.application.MachineLearning.experiment.experiment import Experiment


def doTest():
    italy_league = League.read_by_name("Italy", like=True)[0]
    exp = Experiment(1)
    exp.run(italy_league, complete=True)


doTest()
