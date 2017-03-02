import logging
import numpy as np

from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm
from src.application.Exception.MLException import MLException
import src.util.util as util

log = logging.getLogger(__name__)


class Poisson(MachineLearningAlgorithm):
    def __init__(self, method
                     , train_data
                     , train_label
                     , test_data
                     , test_label
                     , train_description
                     , test_description
                     , **params):
        MachineLearningAlgorithm.__init__(self,
                                          train_data,
                                          train_label,
                                          test_data,
                                          test_label,
                                          train_description,
                                          test_description)
        self.method = method
        self.estimator = None
        self.params = params

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
        predicted = self.estimator.predict(data)
        probs = self.estimator.predict_proba(data)

        predicted_labels = []
        probability_events = []

        for k, v in enumerate(predicted):
            predicted_labels.append(v)
            probability_events.append(probs[k][np.where(self.estimator.classes_ == v)][0])

        return predicted_labels, probability_events
