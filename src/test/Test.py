import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


from src.application.input_preprocess.MatchesResultManagement import MatchesResultReader
import src.application.MachineLearning.MachineLearningInput as MLInput
import src.application.MachineLearning.MachineLearningAlgorithm as MachineLearningAlgorithm


def doTest():
    matches, labels, matches_names = MLInput.get_datas()

    #mag = MachineLearningAlgorithm.get_machine_learning_algorithm("Sklearn", "SVC", matches, labels, matches_names)
    mag = MachineLearningAlgorithm.get_machine_learning_algorithm("TensorFlow", "SVC", matches, labels, matches_names)

    mag.train()
    mag.score()
    #labels, probs, event_description = mag.predict()

    # for k,v in enumerate(labels):
    #   print(event_description[k], v, probs[k])


doTest()


