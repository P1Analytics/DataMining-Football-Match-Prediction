import src.application.Domain.Team as Team
import src.application.Domain.League as League
import sklearn
from sklearn.model_selection import train_test_split
import numpy as np
from matplotlib import pyplot as plt
from sklearn import svm

italy_league = League.read_all()[4]
teams = italy_league.get_teams("2015/2016")

for t in teams:
    print(t.team_long_name)

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
for match in italy_league.get_matches(season="2015/2016"):
    home_team = match.get_home_team()
    away_team = match.get_away_team()

    #matches.append([goal_done[home_team.team_long_name],goal_received[home_team.team_long_name],goal_done[away_team.team_long_name],goal_received[away_team.team_long_name]])
    matches.append([goal_done[home_team.team_long_name]- goal_received[home_team.team_long_name],
                    goal_done[away_team.team_long_name]- goal_received[away_team.team_long_name]])

    if match.home_team_goal > match.away_team_goal:
        labels.append(1)
    else:
        labels.append(0)

for i,m in enumerate(matches):
    print(m, labels[i])

for t in teams:
    print(t.team_long_name, "["+str(goal_done[t.team_long_name])+", "+str(goal_received[t.team_long_name])+"]")


matches = np.asarray(matches)
labels = np.asarray(labels)
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
    plt.show()

print(rbfaccuracyArray)
plt.figure()