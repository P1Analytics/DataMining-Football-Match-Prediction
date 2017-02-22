import src.application.MachineLearning.MachineLearningInput as MLInput
import src.application.MachineLearning.MachineLearningAlgorithm as MachineLearningAlgorithm
import src.application.Domain.League as League
import src.util.util as util

from src.application.Exception.MLException import MLException

import matplotlib.pyplot as plt


def doTest():
    italy_league = League.read_by_name("Italy", like=True)[0]
    print("League: "+italy_league.name)

    for season in italy_league.get_seasons():
        dict_to_plot = dict()
        average_accuracy = dict()
        print()
        print("Elaborating season:\t", season)
        for stage in range(1, 39):
            print()
            print("Predicting stage\t", stage)

            try:
                for representation in range(1, 5):
                    matches, labels, matches_names, matches_to_predict, matches_to_predict_names, labels_to_preidct = \
                        MLInput.team_home_away_form(italy_league,
                        # MLInput.team_form(italy_league,
                                          representation,
                                          stage,
                                          stages_to_train=10,     # numer of stages to consider --> it define the size of the train (EX: 38 * 10 train input)
                                          season=season)

                    params = {"number_step": 1000, "kernel": "rbf", "k": 9}

                    accuracy = MachineLearningAlgorithm.run_predict_all_algorithms(matches,
                                                                                   labels,
                                                                                   matches_to_predict,
                                                                                   labels_to_preidct,
                                                                                   matches_names,
                                                                                   matches_to_predict_names,
                                                                                   False,
                                                                                   **params)

                    print(stage, len(matches), representation, accuracy)
                    try:
                        dict_to_plot[representation].append(dict_to_plot[representation][-1]+accuracy)

                        average_accuracy[representation][0] += 1
                        average_accuracy[representation][1] += accuracy
                    except KeyError:
                        dict_to_plot[representation] = []
                        dict_to_plot[representation].append(accuracy)

                        average_accuracy[representation] = [1, accuracy]

                print("average accuracy", average_accuracy)

            except MLException:
                print("No data to predict", season, stage)
                continue

        fig = plt.figure()
        plt.title(italy_league.name+" ["+season+"]")
        #plt.plot(average_accuracy[1][1], label='r1')
        #plt.plot(average_accuracy[2][1], label='r2')
        #plt.plot(average_accuracy[3][1], label='r3')
        #plt.plot(average_accuracy[4][1], label='r4')
        plt.plot(range(stage, stage+len(dict_to_plot[1])), dict_to_plot[1], marker='o', linestyle='-', label='r1, '+str(round(average_accuracy[1][1]/average_accuracy[1][0],2)))
        plt.plot(range(stage, stage+len(dict_to_plot[2])), dict_to_plot[2], marker='o', linestyle='-', label='r2, '+str(round(average_accuracy[2][1]/average_accuracy[2][0],2)))
        plt.plot(range(stage, stage+len(dict_to_plot[3])), dict_to_plot[3], marker='o', linestyle='-', label='r3, '+str(round(average_accuracy[3][1]/average_accuracy[3][0],2)))
        plt.plot(range(stage, stage+len(dict_to_plot[4])), dict_to_plot[4], marker='o', linestyle='-', label='r4, '+str(round(average_accuracy[4][1]/average_accuracy[4][0],2)))

        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        fig.savefig(util.get_project_directory()+"data/figure/fig_"+season.replace('/','_')+"_"+str(stage)+".png", bbox_inches='tight')
        plt.close()





    '''
    matches, labels, matches_names = MLInput.get_datas_by_team("45", "2015/2016", 3)
    #matches, labels, matches_names = MLInput.team_form("Italy Serie A", 4, n=None, season="2015/2016")
    #matches, labels, matches_names = MLInput.team_home_away_form("Italy Serie A", 4, n=None, season= "2015/2016")
    #matches, labels, matches_names = MLInput.match_statistics("Italy Serie A", n=None, season="2015/2016")
    params = {"batch_size": 25, "number_step":500, "kernel":"rbf", "k":9}
    MachineLearningAlgorithm.run_all_algorithms(matches, labels, matches_names,False, **params)
    '''


doTest()


