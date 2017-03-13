import src.application.Domain.League as League
from src.application.MachineLearning.experiment.experiment import Experiment
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli

import src.util.util as util
util.init_logger(10)

def do_test_1():
    league = League.read_by_name("Italy", like=True)[0]
    for mtii in [1, 2, 3]:
        for mtir in [1,2,3,4]:
            if mtii == 1 and (mtir == 1 or mtir == 2):
                continue
            params = {"ml_train_input_id": mtii, "ml_train_input_representation": mtir}
            exp = Experiment(1)
            exp.run(league, complete=False, **params)


def doTest():
    league = League.read_by_name("Italy", like=True)[0]

    for i,desc in mli.get_input_ids().items():

        if len(mli.get_representations(i)) == 0:
            params = {"ml_train_input_id": i}
            exp = Experiment(2)
            exp.run(league, complete=True, **params)

        for r in mli.get_representations(i):
            params = {"ml_train_input_id": i, "ml_train_input_representation": r}
            exp = Experiment(2)
            exp.run(league, complete=True, **params)


doTest()
# do_test_1()

