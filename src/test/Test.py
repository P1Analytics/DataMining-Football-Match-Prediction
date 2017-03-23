import src.application.Domain.League as League
from src.application.MachineLearning.experiment.experiment import Experiment
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli

import src.util.util as util
util.init_logger(20)

def do_test_4():
    league = League.read_by_name("ita", like=True)[0]
    #for league in League.read_all():
    print(league.name)
    exp = Experiment(5)
    exp.run(league, complete=True, **{"type_evaluation": 1})


def doTest():
    league = League.read_by_name("Italy", like=True)[0]
    exp = Experiment(0)
    exp.run(league, complete=True, **{"type_evaluation": 4, "ml_train_input_id": 5})



#doTest()
do_test_4()
