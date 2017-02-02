import random
import numpy as np
import src.application.Domain.League as League
import src.application.Domain.Team as Team

from src.application.MachineLearning.my_sklearn.Sklearn import SklearnAlgorithm

class MachineLearningAlgorithm(object):
    def __init__(self, framework, algorithm, data, data_label, train_percentage=0.75, data_description=None):
        self.framework = framework
        self.algorithm = algorithm
        self.learning_algorithm = None

        if data_description:
            train_datas, test_datas = split_data(train_percentage, True, [data, data_label, data_description])
        else:
            train_datas, test_datas = split_data(train_percentage, True, [data, data_label])

        self.train_data = train_datas[0]
        self.train_label = train_datas[1]
        self.test_data = test_datas[0]
        self.test_label = test_datas[1]
        if data_description:
            self.train_description = train_datas[2]
            self.test_description = test_datas[2]
        else:
            self.train_description = ["" for x in range(len(self.train_data))]
            self.train_description = ["" for x in range(len(self.test_data))]

        if framework=="Sklearn":
            if algorithm=="SVC":
                self.learning_algorithm = SklearnAlgorithm(self.train_data, self.train_label, self.test_data, self.test_label)

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
            print(self.train_description[k],"\t",self.test_label[k], "\t", v, "\t", probability_events[k])


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
    mag = MachineLearningAlgorithm("Sklearn","SVC", matches, labels, train_percentage=0.75, data_description=matches_names)
    mag.train()
    mag.score()
    #labels, probs, event_description = mag.predict()

    #for k,v in enumerate(labels):
     #   print(event_description[k], v, probs[k])


test()





