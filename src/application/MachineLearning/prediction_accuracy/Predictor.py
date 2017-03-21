import src.util.util as util
import src.util.Cache as Cache
import src.util.MLUtil as MLUtil
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli
import src.application.Domain.Match as Match
import src.application.Domain.Team as Team
import heapq


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
            return {}

    def get_best_team_predicted(self, league, season, stage, n_teams_returned=3):

        best_teams = dict()
        s = season
        i = 1
        if stage - 1 == 0:
            y = int(s.split("/")[0]) - 1
            s = str(y) + "/" + str(y + 1)
            stage_predictions = league.get_stages_by_season(s)
        else:
            stage_predictions = stage - 1

        while i <= self.ml_train_stages_to_train:
            predictions = self.predict(league, s, stage_predictions)

            for match_id, pair in predictions.items():
                if len(pair) == 0:
                    continue
                match = Match.read_by_match_id(match_id)
                pred_label = pair[0]
                if pred_label == MLUtil.get_label(match):
                    try:
                        best_teams[match.home_team_api_id] += 1
                    except KeyError:
                        best_teams[match.home_team_api_id] = 1
                    try:
                        best_teams[match.away_team_api_id] += 1
                    except KeyError:
                        best_teams[match.away_team_api_id] = 1
            i += 1
            if stage_predictions - i == 0:
                y = int(s.split("/")[0])-1
                s = str(y)+"/"+str(y+1)
                stage_predictions = league.get_stages_by_season(s)
            else:
                stage_predictions -= 1

        h = []
        for team_api_id, accuracy in best_teams.items():
            heapq.heappush(h, (accuracy, team_api_id))

        top_k = [Team.read_by_team_api_id(team_api_id) for a, team_api_id
                 in heapq.nlargest(n_teams_returned, h, lambda x: x[0])[:n_teams_returned]]
        return top_k


def get_predictor(ml_alg_framework="my_poisson",
                  ml_alg_method="SVM",
                  ml_train_input_id=5,
                  ml_train_input_representation=1,
                  ml_train_stages_to_train=19,
                  update_current_predictor=True):
    global current_predictor

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

    if update_current_predictor:
        current_predictor = predictor

    return predictor


current_predictor = get_predictor()


def get_current_predictor():
    global current_predictor
    return current_predictor


def init_predictor():
    print("> Init default predictor")
    date = util.get_date()
    matches = Match.read_by_match_date(date)
    matches = sorted(matches, key=lambda match: match.date)
    predictor = get_predictor()
    for m in matches:
        predictor.predict(m.get_league(), m.season, m.stage)
