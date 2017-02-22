from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import numpy as np

from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm
import src.util.util as util

class SklearnAlgorithm(MachineLearningAlgorithm):
    def __init__(self, method
                     , train_data
                     , train_label
                     , test_data
                     , test_label
                     , train_description
                     , test_description
                     , **params):
        MachineLearningAlgorithm.__init__(self, train_data, train_label, test_data, test_label, train_description, test_description)
        self.method = method
        self.estimator = None
        self.params = params

    def train(self,):
        if self.method == "SVM":
            kernel = util.get_default(self.params, "kernel", "rbf")
            self.estimator = get_SVM_estimator(self.train_data, self.train_label, kernel)


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
    print("SklearnAlgorithm > Starting GridSearchCV to find the best parameter")

    clf = GridSearchCV(svr, parameters)
    clf.fit(train_data, train_label)
    print(clf.cv_results_['params'][clf.best_index_])

    return clf.best_estimator_