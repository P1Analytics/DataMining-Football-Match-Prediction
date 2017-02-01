import src.application.Domain.Team as Team
import src.application.Domain.League as League
import sklearn
from sklearn.model_selection import train_test_split
import numpy as np
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import random


import src.util.util as util
util.init_logger()

italy_league = League.read_all()[4]
teams = italy_league.get_teams("2015/2016")

goal_done = {team.team_long_name:0 for team in teams}
goal_received = {team.team_long_name:0 for team in teams}

for team in teams:
    t = Team.read_by_name(team.team_long_name)
    matches = t.get_matches(ordered=True, season="2015/2016")
    for m in matches:
        if team.team_long_name == m.get_home_team().team_long_name:
            goal_done[team.team_long_name] = goal_done[team.team_long_name]+m.home_team_goal
            goal_received[team.team_long_name] = goal_received[team.team_long_name] + m.away_team_goal
        else:
            goal_done[team.team_long_name] = goal_done[team.team_long_name] + m.away_team_goal
            goal_received[team.team_long_name] = goal_received[team.team_long_name] + m.home_team_goal



print(goal_done)
print(goal_received)

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
    #matches.append([goal_done[home_team.team_long_name],goal_received[home_team.team_long_name],goal_done[away_team.team_long_name],goal_received[away_team.team_long_name]])
    home_goal_done, home_goal_received = home_team.get_goals_by_season_and_stage("2015/2016", match.stage)
    #print(match.stage, home_team.team_long_name, home_goal_done, home_goal_received)
    away_goal_done, away_goal_received = away_team.get_goals_by_season_and_stage("2015/2016", match.stage)
    matches.append(np.asarray([home_goal_done / match.stage, home_goal_received / match.stage, home_team.get_points_by_season_and_stage("2015/2016", match.stage) / match.stage,
                               away_goal_done / match.stage, away_goal_received / match.stage, away_team.get_points_by_season_and_stage("2015/2016", match.stage) / match.stage]))

    matches_names.append(home_team.team_long_name+" vs "+away_team.team_long_name)


matches = np.asarray(matches)
labels = np.asarray(labels)

c = list(zip(matches, labels, matches_names))
random.shuffle(c)
matches, labels, matches_names = zip(*c)


train_size = int(0.75*len(matches))

train_data = matches[:train_size]
train_label = labels[:train_size]
train_matches = matches_names[:train_size]

test_data = matches[train_size:]
test_label = labels[train_size:]
test_matches = matches_names[train_size:]

Cs = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
gammas = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]

parameters = {'kernel':('rbf',), 'C':Cs, 'gamma':gammas}
svr = SVC(probability=True)
clf = GridSearchCV(svr, parameters)
clf.fit(train_data, train_label)
print (clf.cv_results_['params'][clf.best_index_])
estimator = clf.best_estimator_
estimator.fit(train_data, train_label)

classifier_score = estimator.score(test_data, test_label)
print(classifier_score)
predicted = estimator.predict(test_data)
probs = estimator.predict_proba(test_data)
for k,v in enumerate(predicted):
    print(test_matches[k], test_label[k], "Predicted:", v, "P("+str(np.where(estimator.classes_ == v)[0])+")",str(probs[k][np.where(estimator.classes_ == v)][0]))




'''
X_train, X_test, y_train, y_test = train_test_split( matches, labels, test_size=0.33, random_state=42)

print(X_train)
print(X_test)
print(y_train)
print(y_test)

h = 0.02

x_min, x_max = matches[:, 0].min() - 1, matches[:, 0].max() + 1
y_min, y_max = matches[:, 1].min() - 1, matches[:, 1].max() + 1

xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))


rbfaccuracyArray = []

for i in range(-3, 4):
    myAccuracy = []

    plt.figure()
    c = 10 ** i;
    rbfSVN = svm.SVC(kernel='rbf', C=c).fit(X_train, y_train.ravel())
    accuracy = rbfSVN.score(X_test, y_test.ravel())
    testArray = rbfSVN.predict(X_test)
    counter = 0
    for yr,y in zip(y_test,testArray):
        print(yr, y)
        if(yr == y):
            counter+= 1
    result = float(counter)/float(len(y_test))
    print("percentuage of correct prediction: ", result)
    myAccuracy.append(c)
    myAccuracy.append(accuracy)
    rbfaccuracyArray.append(myAccuracy)
    Z = rbfSVN.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
    plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=plt.cm.coolwarm)
    plt.title("RBF Kernel C: " + str(c))
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    print("showing...")
    plt.show(block=True)

print(rbfaccuracyArray)
plt.figure()
'''