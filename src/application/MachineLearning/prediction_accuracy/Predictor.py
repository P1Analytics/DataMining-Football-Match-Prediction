import src.util.util as util
import src.application.MachineLearning.experiment.experiment as experiment
from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli
import src.application.Domain.Match as Match
import src.application.Domain.League as League
import src.util.MLUtil as MLUtil
import src.util.Cache as Cache


class Predictor(object):
    def __init__(self, ml_alg_framework,
                       ml_alg_method,
                       ml_train_input_id,
                       ml_train_input_representation,
                       ml_train_stages_to_train):

        self.ml_alg_method = ml_alg_method
        self.ml_alg_framework = ml_alg_framework
        self.ml_train_input_id = ml_train_input_id
        self.ml_train_input_representation = ml_train_input_representation
        self.ml_train_stages_to_train = ml_train_stages_to_train

        key = self.get_predictor_key()

        # KEY: LEAGUE ID;  VALUE: <MATCH ID: <pred, prob>>
        self.predictions = dict()
        Cache.add_element(key, self, "PREDICTOR_BY_KEY")

    def get_predictor_key(self):
        key = ""
        key += self.ml_alg_framework+"_"
        key += self.ml_alg_method+"_"
        key += str(self.ml_train_input_id)+"_"
        key += str(self.ml_train_input_representation)+"_"
        key += str(self.ml_train_stages_to_train)

        return key

    def predict(self, league, season, stage):
        try:
            self.predictions[league.id]
        except KeyError:
            self.predictions[league.id] = dict()

        this_predictions = dict()
        try:
            for match_id, p in self.predictions[league.id].items():
                match = Match.read_by_match_id(match_id)
                if match.season == season and match.stage == stage:
                    this_predictions[match_id] = p
        except KeyError:
            pass

        if len(this_predictions) > 0:
            return this_predictions
        this_predictions[league.id] = dict()

        try:
            matches, labels, matches_id, matches_to_predict, matches_to_predict_id, labels_to_predict = \
                mli.get_input_to_train(self.ml_train_input_id,
                                       league,
                                       self.ml_train_input_representation,
                                       stage,
                                       self.ml_train_stages_to_train,
                                       season)

            ml_alg = mla.get_machine_learning_algorithm(self.ml_alg_framework,
                                                        self.ml_alg_method,
                                                        matches,
                                                        labels,
                                                        matches_id,
                                                        train_percentage=1,
                                                        )

            ml_alg.train()
            predicted_labels, probability_events = ml_alg.predict(matches_to_predict)

            for match_id, prediction, probability in zip(matches_to_predict_id, predicted_labels, probability_events):
                this_predictions[match_id] = [prediction, probability]
                self.predictions[league.id][match_id] = [prediction, probability]

            return this_predictions
        except Exception as e:
            print(e)
            return {}


def get_predictor(ml_alg_framework="my_poisson",
                  ml_alg_method="SVM",
                  ml_train_input_id=5,
                  ml_train_input_representation=1,
                  ml_train_stages_to_train=20):
    key = ""
    key += ml_alg_framework+"_"
    key += ml_alg_method+"_"
    key += str(ml_train_input_id)+"_"
    key += str(ml_train_input_representation)+"_"
    key += str(ml_train_stages_to_train)

    try:
        return Cache.get_element(key, "PREDICTOR_BY_KEY")
    except KeyError:
        pass

    predictor = Predictor(ml_alg_framework,
                  ml_alg_method,
                  ml_train_input_id,
                  ml_train_input_representation,
                  ml_train_stages_to_train)

    return predictor
