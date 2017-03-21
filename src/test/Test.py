import src.application.Domain.League as League
from src.application.MachineLearning.experiment.experiment import Experiment
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli

import src.util.util as util
util.init_logger(20)

def do_test_0():
    league = League.read_by_name("italy", like=True)[0]
    exp = Experiment(0)
    exp.run(league, complete=True, **{"type_evaluation": 5})


def doTest():
    league = League.read_by_name("Italy", like=True)[0]

    for i,desc in mli.get_input_ids().items():
        if i!=4:
            continue
        if len(mli.get_representations(i)) == 0:
            params = {"ml_train_input_id": i}
            exp = Experiment(2)
            exp.run(league, complete=True, **params)

        for r in mli.get_representations(i):
            params = {"ml_train_input_id": i, "ml_train_input_representation": r}
            exp = Experiment(2)
            exp.run(league, complete=True, **params)


#doTest()
do_test_0()

