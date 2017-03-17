import logging
import numpy as np

from numpy.random import poisson

from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm
from src.application.Exception.MLException import MLException
import src.util.util as util

log = logging.getLogger(__name__)


class Poisson(MachineLearningAlgorithm):
    def __init__(self, **params):
        MachineLearningAlgorithm.__init__(self,
                                          [],
                                          [],
                                          [],
                                          [],
                                          [],
                                          [])
        self.params = params

        self.number_sample = util.get_default(params, "poisson_n_sample", 10000)

    def train(self,):
        pass

    def score(self):
        predicted, probs = self.predict(self.test_data)

        predicted_labels = []
        probability_events = []

        for k, v in enumerate(predicted):
            predicted_labels.append(v)
            probability_events.append(probs[k][np.where(self.estimator.classes_ == v)][0])

        return self.post_score(predicted_labels, probability_events)

    def predict(self, data):

        predicted_labels = []
        probability_events = []

        for exp in data:
            outcomes_0 = poisson(exp[0], self.number_sample)
            outcomes_1 = poisson(exp[1], self.number_sample)

            prob_dist_0 = get_probability(outcomes_0)
            prob_dist_1 = get_probability(outcomes_1)

            event_prob = get_event_probability(prob_dist_0, prob_dist_1)
            predicted_label, prob = predict(event_prob)

            predicted_labels.append(predicted_label)
            probability_events.append(prob)

        return predicted_labels, probability_events


def predict(event_prob):
    p_max = 0
    label = None

    for event_outcome, prob in event_prob.items():
        if prob > p_max:
            p_max = prob
            label = event_outcome

    return label, p_max


def get_probability(outcomes):
    outcome_counter = dict()
    count = 0
    for outcome in outcomes:
        count += 1
        try:
            outcome_counter[outcome] += 1
        except KeyError:
            outcome_counter[outcome] = 1

    res = dict()
    for k,v in outcome_counter.items():
        res[k] = v/count
    return res


def get_event_probability(g1_prob, g2_prob):
    prob_1 = 0
    prob_X = 0
    prob_2 = 0
    for hg, phg in g1_prob.items():
        for ag, pag in g2_prob.items():
            if hg > ag:
                prob_1 += phg*pag
            elif hg < ag:
                prob_2 += phg*pag
            else:
                prob_X += phg * pag

    return {1:prob_1, 0:prob_X, 2:prob_2}
