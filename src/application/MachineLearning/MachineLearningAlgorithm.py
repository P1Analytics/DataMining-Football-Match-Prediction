import random
import numpy as np
import src.application.Domain.League as League
import src.application.Domain.Team as Team
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

class SklearnAlgorithm(object):
    def __init__(self, data, label, train_percentage = 0.75, data_description=None):

        if data_description:
            train_data, test_data = split_data(train_percentage, True, [data, label, data_description])
        else:
            train_data, test_data = split_data(train_percentage, True, [data, label])

        self.train_data = train_data
        self.test_data = test_data


    def train(self,):
        Cs = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
        gammas = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]

        parameters = {'kernel': ('rbf',), 'C': Cs, 'gamma': gammas}
        svr = SVC(probability=True)
        clf = GridSearchCV(svr, parameters)
        clf.fit(self.train_data[0], self.train_data[1])
        print(clf.cv_results_['params'][clf.best_index_])
        self.estimator = clf.best_estimator_

    def score(self):
        classifier_score = self.estimator.score(self.test_data[0], self.test_data[1])
        print("Score is ", classifier_score)

    def predict(self, data=None):
        if not data:
            data = self.test_data[0]
        label = self.test_data[1]
        predicted = self.estimator.predict(data)
        probs = self.estimator.predict_proba(data)

        predicted_labels = []
        probability_events = []
        event_description = []

        for k, v in enumerate(predicted):
            if len(self.test_data)>2:
                event_description.append(self.test_data[2][k])
            predicted_labels.append(v)
            probability_events.append(probs[k][np.where(self.estimator.classes_ == v)][0])

        for k, v in enumerate(predicted_labels):
            print(event_description[k],"\t" ,label[k],"\t" , v,"\t" , probability_events[k])

        return predicted_labels, probability_events, event_description


class MachineLearningAlgorithm(object):
    def __init__(self, framework, algorithm, data, labels, data_description=None):
        self.framework = framework
        self.algorithm = algorithm
        self.learning_algorithm = None
        if framework=="Sklearn":
            if algorithm=="SVC":
                self.learning_algorithm = SklearnAlgorithm(data, labels, data_description=data_description)

        if not self.learning_algorithm:
            # Use default learning algorithm
            self.learning_algorithm = SklearnAlgorithm(data, labels, data_description=data_description)


    def train(self, ):
        self.learning_algorithm.train()

    def score(self):
        self.learning_algorithm.score()

    def predict(self, data=None):
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
    italy_league = League.read_all()[4]
    teams = italy_league.get_teams("2015/2016")

    goal_done = {team.team_long_name: 0 for team in teams}
    goal_received = {team.team_long_name: 0 for team in teams}

    for team in teams:
        t = Team.read_by_name(team.team_long_name)
        matches = t.get_matches(ordered=True, season="2015/2016")
        for m in matches:
            if team.team_long_name == m.get_home_team().team_long_name:
                goal_done[team.team_long_name] = goal_done[team.team_long_name] + m.home_team_goal
                goal_received[team.team_long_name] = goal_received[team.team_long_name] + m.away_team_goal
            else:
                goal_done[team.team_long_name] = goal_done[team.team_long_name] + m.away_team_goal
                goal_received[team.team_long_name] = goal_received[team.team_long_name] + m.home_team_goal

    # represent a match as [HTGD, HTGR, ATGD, ATGR], label them with 1 (home team win), -1 oterwise

    matches = []
    labels = []
    matches_names = []
    for match in italy_league.get_matches(season="2015/2016"):
        home_team = match.get_home_team()
        away_team = match.get_away_team()
        label = 0
        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        else:
            labels.append(0)
        # matches.append([goal_done[home_team.team_long_name],goal_received[home_team.team_long_name],goal_done[away_team.team_long_name],goal_received[away_team.team_long_name]])
        home_goal_done, home_goal_received = home_team.get_goals_by_season_and_stage("2015/2016", match.stage)
        # print(match.stage, home_team.team_long_name, home_goal_done, home_goal_received)
        away_goal_done, away_goal_received = away_team.get_goals_by_season_and_stage("2015/2016", match.stage)
        matches.append(np.asarray([home_goal_done / match.stage, home_goal_received / match.stage,
                                   home_team.get_points_by_season_and_stage("2015/2016", match.stage) / match.stage,
                                   away_goal_done / match.stage, away_goal_received / match.stage,
                                   away_team.get_points_by_season_and_stage("2015/2016", match.stage) / match.stage]))

        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

    matches = np.asarray(matches)
    labels = np.asarray(labels)
    mag = MachineLearningAlgorithm("Sklearn","SVC", matches, labels, matches_names)
    mag.train()
    mag.score()
    labels, probs, event_description = mag.predict()

    #for k,v in enumerate(labels):
     #   print(event_description[k], v, probs[k])


test()





