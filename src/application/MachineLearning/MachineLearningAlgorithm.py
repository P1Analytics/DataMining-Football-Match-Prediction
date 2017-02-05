import random
import numpy as np

class MachineLearningAlgorithm(object):

    def __init__(self, train_data, train_label, test_data, test_label, train_descirption, test_description):

        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_label = test_label
        self.train_description = train_descirption
        self.test_description = test_description

    def train(self, ):
        raise NotImplementedError

    def post_score(self, predicted_labels, probability_events):

        accuracy = 0
        for k, v in enumerate(predicted_labels):
            if v == self.test_label[k]:
                accuracy += 1
        print("Accuracy", accuracy/len(predicted_labels))

        for k, v in enumerate(predicted_labels):
            print(self.test_description[k],"\t",self.test_label[k], "\t", v, "\t", probability_events[k])

        return predicted_labels, probability_events

    def predict(self, data):
        raise NotImplementedError



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


from src.application.MachineLearning.my_sklearn.Sklearn import SklearnAlgorithm
from src.application.MachineLearning.my_tensor_flow.TensorFlow import TensorFlow
from src.application.MachineLearning.my_tensor_flow.NNAlgorithm import NNAlgorithm

def get_machine_learning_algorithm(framework, method, data, data_label, data_description=None, train_percentage=0.75, **params):

    if data_description:
        train_datas, test_datas = split_data(train_percentage, True, [data, data_label, data_description])
    else:
        train_datas, test_datas = split_data(train_percentage, True, [data, data_label])

    train_data = np.asarray(train_datas[0])
    train_label = np.asarray(train_datas[1])
    test_data = np.asarray(test_datas[0])
    test_label = np.asarray(test_datas[1])
    if data_description:
        train_description = train_datas[2]
        test_description = test_datas[2]
    else:
        train_description = ["" for x in range(len(train_data))]
        test_description = ["" for x in range(len(test_data))]

    if framework == "Sklearn":
        learning_algorithm = SklearnAlgorithm(method, train_data, train_label, test_data, test_label, train_description, test_description, **params)

    elif framework == "TensorFlow":
        if method == "SVM":
            learning_algorithm = TensorFlow(method, train_data, train_label, test_data, test_label, train_description, test_description, **params)
        elif method == "KNN":
            learning_algorithm = NNAlgorithm( train_data, train_label, test_data, test_label)
    else:
        learning_algorithm = SklearnAlgorithm(method, train_data, train_label, test_data, test_label, train_description, test_description, **params)

    return learning_algorithm


def run_all_algorithms(data, data_label, data_description=None, train_percentage=0.75, **params):

    if data_description:
        train_datas, test_datas = split_data(train_percentage, True, [data, data_label, data_description])
    else:
        train_datas, test_datas = split_data(train_percentage, True, [data, data_label])

    train_data = np.asarray(train_datas[0])
    train_label = np.asarray(train_datas[1])
    test_data = np.asarray(test_datas[0])
    test_label = np.asarray(test_datas[1])

    if data_description:
        train_description = train_datas[2]
        test_description = test_datas[2]
    else:
        train_description = ["" for x in range(len(train_data))]
        test_description = ["" for x in range(len(test_data))]

    mag = NNAlgorithm( train_data, train_label, test_data, test_label)
    mag.train()
    mag.score()

    mag = TensorFlow("SVM", train_data, train_label, test_data, test_label, train_description, test_description, **params)
    mag.train()
    mag.score()

    mag = SklearnAlgorithm("SVM", train_data, train_label, test_data, test_label, train_description, test_description, **params)
    mag.train()
    mag.score()

