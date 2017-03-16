from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

import logging
import numpy as np

from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm
from src.application.Exception.MLException import MLException
import src.util.util as util

log = logging.getLogger(__name__)


class SklearnAlgorithm(MachineLearningAlgorithm):
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
        if self.method == "SVM":
            kernel = util.get_default(self.params, "kernel", "rbf")
            self.estimator = get_SVM_estimator(self.train_data, self.train_label, kernel)

        elif self.method == "KNN":
            self.estimator = get_KNeighborsClassifier(self.train_data, self.train_label)

        elif self.method == "RandomForest":
            # self.estimator = get_RandomForestClassifier(self.train_data, self.train_label)
            self.estimator = RandomForestClassifier()
            self.estimator.fit(self.train_data, self.train_label)

        elif self.method == "AdaBoostClassifier":
            self.estimator = AdaBoostClassifier(DecisionTreeClassifier(max_depth=5),
                                                n_estimators=1000, learning_rate=0.1, random_state=42)
            self.estimator.fit(self.train_data, self.train_label)

        else:
            raise MLException(4)

    def score(self):
        predicted = self.estimator.predict(self.test_data)
        probs = self.estimator.predict_proba(self.test_data)

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


def get_SVM_estimator(train_data, train_label, kernel):
    Cs = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
    gammas = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]

    parameters = {'kernel': (kernel,), 'C': Cs, 'gamma': gammas}
    svr = SVC(probability=True)
    log.debug("SklearnAlgorithm > Starting GridSearchCV to find the best parameter")

    clf = GridSearchCV(svr, parameters)
    clf.fit(train_data, train_label)
    log.debug(clf.cv_results_['params'][clf.best_index_])

    return clf.best_estimator_


def get_KNeighborsClassifier(train_data, train_label):
    parameter = {'weights':['uniform', 'distance'], 'n_neighbors':[5,7,9,11,13,15,21,31]}
    clf = GridSearchCV(KNeighborsClassifier(), parameter)
    clf.fit(train_data, train_label)

    log.debug(clf.cv_results_['params'][clf.best_index_])
    return clf.best_estimator_


def get_RandomForestClassifier(train_data, train_label):
    parameter = {'n_estimators':[5,10,15],'max_features':['auto','sqrt','log2'],'min_samples_split':[0.1,0.25,0.4,0.5]}
    clf = GridSearchCV(RandomForestClassifier(), parameter)
    clf.fit(train_data, train_label)

    log.debug(clf.cv_results_['params'][clf.best_index_])
    return clf.best_estimator_
