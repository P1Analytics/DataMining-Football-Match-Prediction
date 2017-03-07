import src.application.Domain.League as League
from src.application.MachineLearning.experiment.experiment import Experiment

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

    exp = Experiment(1)
    params = {"ml_alg_method":"MultiLayer", "ml_alg_framework":"poisson", "ml_train_stages_to_train":20,
              "ml_train_input_id":5}
    exp.run(league, complete=True, **params)


doTest()
# do_test_1()

