import random
import numpy as np

from src.application.MachineLearning.my_sklearn.Sklearn import SklearnAlgorithm
from src.application.MachineLearning.my_tensor_flow.TensorFlow import TensorFlow
import src.application.MachineLearning.MachineLearningInput as MLInput

class MachineLearningAlgorithm(object):
    def __init__(self, framework, algorithm, data, data_label, train_percentage=0.75, data_description=None):
        self.framework = framework
        self.algorithm = algorithm
        self.learning_algorithm = None

        if data_description:
            train_datas, test_datas = split_data(train_percentage, True, [data, data_label, data_description])
        else:
            train_datas, test_datas = split_data(train_percentage, True, [data, data_label])

        self.train_data = np.asarray(train_datas[0])
        self.train_label = np.asarray(train_datas[1])
        self.test_data = np.asarray(test_datas[0])
        self.test_label = np.asarray(test_datas[1])
        if data_description:
            self.train_description = train_datas[2]
            self.test_description = test_datas[2]
        else:
            self.train_description = ["" for x in range(len(self.train_data))]
            self.train_description = ["" for x in range(len(self.test_data))]

        if framework=="Sklearn":
            if algorithm=="SVC":
                self.learning_algorithm = SklearnAlgorithm(self.train_data, self.train_label, self.test_data, self.test_label)
        elif framework=="TensorFlow":
            self.learning_algorithm = TensorFlow(self.train_data, self.train_label, self.test_data,
                                                       self.test_label)

        if not self.learning_algorithm:
            # Use default learning algorithm
            self.learning_algorithm = SklearnAlgorithm(self.train_data, self.train_label, self.test_data, self.test_label)


    def train(self, ):
        self.learning_algorithm.train()

    def score(self):
        predicted_labels, probability_events = self.learning_algorithm.score()

        accuracy = 0
        for k, v in enumerate(predicted_labels):
            if v == self.test_label[k]:
                accuracy += 1
        print("AAA accuracy", accuracy/len(predicted_labels))

        for k, v in enumerate(predicted_labels):
            print(self.test_description[k],"\t",self.test_label[k], "\t", v, "\t", probability_events[k])


    def predict(self, data):
        return self.learning_algorithm.predict(data)


def split_data(split_percentage=0.75, shuffle=True, *datas):
    '''

    :param train_percentage:
    :param shuffle:
    :param datas:
    :return:
    '''
    data_size = len(datas[0][0])
    for data in datas[0]:
        if len(data)!=data_size:
            raise Exception("Input data with different length")

    split_size = int(split_percentage * data_size)
    if shuffle:
        c = list(zip(*datas[0]))
        random.shuffle(c)
        datas = list(zip(*c))

    train_datas = []
    test_datas = []
    for data in datas:
        train_datas.append(data[:split_size])
        test_datas.append(data[split_size:])

    return train_datas, test_datas



def test():
    matches, labels, matches_names = MLInput.get_datas()
    #mag = MachineLearningAlgorithm("Sklearn","SVC", matches, labels, train_percentage=0.75, data_description=matches_names)
    mag = MachineLearningAlgorithm("TensorFlow", "SVC", matches, labels, train_percentage=0.75,
                                  data_description=matches_names)
    mag.train()
    mag.score()
    #labels, probs, event_description = mag.predict()

    #for k,v in enumerate(labels):
     #   print(event_description[k], v, probs[k])


test()





