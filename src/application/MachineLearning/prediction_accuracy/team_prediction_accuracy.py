class TeamPredictionAccuracy(object):

    def __init__(self,team, succesfull_predicted_label, played_game):
        self.team = team
        self.succesfull_predicted_label = succesfull_predicted_label
        self.played_game = played_game