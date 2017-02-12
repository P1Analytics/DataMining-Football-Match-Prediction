import matplotlib.pyplot as plt
import numpy as np

class Plot(object):
    def __init__(self,data):
        self.data = data

    def define_grid(self):
        x_min, x_max = self.data[:, 0].min() - 1, self.data[:, 0].max() + 1
        y_min, y_max = self.data[:, 1].min() - 1, self.data[:, 1].max() + 1
        self.xx, self.yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                             np.arange(y_min, y_max, 0.02))
        self.grid_points = np.c_[self.xx.ravel(), self.yy.ravel()]

    def show_decision_bounduaries(self,grid_predictions, data, label):
        grid_predictions = grid_predictions.reshape(self.xx.shape)
        plt.figure()
        plt.contourf(self.xx, self.yy, grid_predictions, cmap=plt.cm.coolwarm, alpha=0.8)
        plt.scatter(data[:, 0], data[:, 1], c=label)
        plt.show()
