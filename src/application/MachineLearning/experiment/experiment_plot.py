import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import numpy as np
import src.util.util as util

class PlotExperiment(object):
    def __init__(self, experiment_type, y, x=None, **params):
        self.y = y
        self.x = x
        self.experiment_type = experiment_type
        self.params = params

        self.fig, self.ax = plt.subplots()
        fig = plt.gcf()
        #size = fig.get_size_inches() * fig.dpi  # size in pixels
        fig.set_size_inches(16, 9)
        #print(fig.get_size_inches(), fig.dpi)

    def plot(self, path_file=True):

        N = len(self.y)
        y_values = [y for y in self.y]

        ind = np.asarray([n*2 for n in range(N)])  # the x locations for the groups
        width = 0.5  # the width of the bars

        rects1 = self.ax.bar(ind, y_values, width, color='r')

        # women_means = (25, 32, 34, 20, 25)
        # women_std = (3, 5, 2, 3, 3)
        # rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)

        # add some text for labels, title and axes ticks
        self.ax.set_xlabel(self.get_x_label())
        self.ax.set_ylabel(self.get_y_label())
        self.ax.set_title(self.get_title())
        self.ax.set_xticks(ind + width / 2)
        if self.x:
            self.ax.set_xticklabels([x for x in self.x])

        # ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))
        self.ax.legend((rects1,), (self.get_y_label(),))
        plt.grid()

        if path_file:
            self.save_fig(path_file)
        else:
            plt.show()

    def get_x_label(self):
        if self.experiment_type == 0:
            return "Stage"
        else:
            raise ValueError

    def get_y_label(self):
        if self.experiment_type == 0:
            return "Accuracy"
        else:
            raise ValueError

    def get_title(self):
        if self.experiment_type == 0:
            return "Stage accuracy of the season "+util.get_default(self.params, "season", "")
        else:
            raise ValueError

    def save_fig(self, path_file):
        self.fig.savefig(path_file)
        plt.close()