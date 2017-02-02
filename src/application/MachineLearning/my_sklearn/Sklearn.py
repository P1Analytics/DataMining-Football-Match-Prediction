from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import numpy as np

class SklearnAlgorithm(object):
    def __init__(self, train_data, train_label, test_data, test_label):

        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_label = test_label

    def train(self,):
        Cs = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
        gammas = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]

        parameters = {'kernel': ('rbf',), 'C': Cs, 'gamma': gammas}
        svr = SVC(probability=True)
        print("SklearnAlgorithm > Starting GridSearchCV to find the best parameter")
        clf = GridSearchCV(svr, parameters)
        clf.fit(self.train_data, self.train_label)
        print(clf.cv_results_['params'][clf.best_index_])
        self.estimator = clf.best_estimator_

    def score(self):
        predicted = self.estimator.predict(self.test_data)
        probs = self.estimator.predict_proba(self.test_data)

        predicted_labels = []
        probability_events = []

        for k, v in enumerate(predicted):
            predicted_labels.append(v)
            probability_events.append(probs[k][np.where(self.estimator.classes_ == v)][0])

        return predicted_labels, probability_events


    def predict(self, data):
        predicted = self.estimator.predict(data)
        probs = self.estimator.predict_proba(data)

        predicted_labels = []
        probability_events = []

        for k, v in enumerate(predicted):
            predicted_labels.append(v)
            probability_events.append(probs[k][np.where(self.estimator.classes_ == v)][0])

        return predicted_labels, probability_events