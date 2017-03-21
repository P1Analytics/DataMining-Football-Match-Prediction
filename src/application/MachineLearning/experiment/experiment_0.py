import src.util.util as util
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli
import src.application.Domain.Match as Match
import src.util.MLUtil as MLUtil
import src.application.MachineLearning.prediction_accuracy.Predictor as Predictor


class stage_bet(object):
    # list of marches we bet on
    def __init__(self, stage, type_evaluation):
        self.stage = stage
        self.type_evaluation = type_evaluation
        self.matches = []       # matches we bet on

        self.profit = 0
        self.invest = 0

    def add_bet(self, prob, profit, bet_odd=None):
        if self.type_evaluation == 5:
            if len(self.matches) == 0:
                self.invest += 1
                self.profit += profit
                self.matches = [(prob, bet_odd)]

            elif prob * bet_odd > self.matches[0][0] * self.matches[0][1]:
                self.profit = self.profit - self.matches[0][1] + profit
                self.matches = [(prob, bet_odd)]

        if self.type_evaluation == 6:
            if bet_odd < 1.26:
                if len(self.matches) == 0:
                    self.invest += 1
                    self.profit += profit
                    self.matches = [(prob, profit)]
                else:
                    self.profit *= bet_odd
                    self.matches.append((prob, profit))



        else:
            self.invest += 1
            self.profit += profit

    def get_profit(self):
        return self.profit

    def get_invest(self):
        return self.invest



def run_experiment_0(exp, league, type_evaluation, **params):

    predictor = Predictor.get_predictor()

    for season in league.get_seasons():
        if season != "2015/2016":
            continue

        invest = 0
        profit = 0

        print(season)
        if season == util.get_current_season():
            break

        for stage in range(1, league.get_stages_by_season(season)+1):

            # KEY: match id     VALUE: <prediction, probability>
            stage_predictions = predictor.predict(league, season, stage, **params)
            current_stage_bet = stage_bet(stage, type_evaluation)

            for match_id, pair in stage_predictions.items():
                if len(pair) == 0:
                    continue
                match = Match.read_by_match_id(match_id)
                if util.is_None(match.B365H) or util.is_None(match.B365D) or util.is_None(match.B365A):
                    continue

                predicted_label = pair[0]
                if predicted_label == 1:
                    bet_odd = match.B365H
                elif predicted_label == 0:
                    bet_odd = match.B365D
                else:
                    bet_odd = match.B365A
                prob = pair[1]
                label = MLUtil.get_label(match)
                m_accuracy, m_invest, m_profit = evaluate_bet(predictor, type_evaluation, label, match, predicted_label, prob)

                if type_evaluation == 5:
                    if m_invest == 1:
                        current_stage_bet.add_bet(prob, m_profit, bet_odd)

                elif type_evaluation == 6:
                    current_stage_bet.add_bet(prob, m_profit, bet_odd)

                elif m_invest == 1:
                        current_stage_bet.add_bet(prob, m_profit)

            profit += current_stage_bet.get_profit()
            invest += current_stage_bet.get_invest()
            print(stage, "\t",str(round(profit-invest,2)).replace(".",","))
        print("Final investment:\t",invest)
        print("Final profit:\t", profit)


def evaluate_bet(predictor, type_evaluation, label, match, predicted_label, prob):

    if type_evaluation == 1:
        # flat bet
        profit = 0
        accuracy = 0
        if label == predicted_label:
            accuracy = 1
            if label == 1:
                profit = match.B365H
            elif label == 0:
                profit = match.B365D
            else:
                profit = match.B365A
        return accuracy, 1, profit

    elif type_evaluation == 2:
        # smart bet
        if (predicted_label == 1 and prob < 1/match.B365H) \
            or (predicted_label == 0 and prob < 1 / match.B365D) \
                or (predicted_label == 2 and prob < 1 / match.B365A):
            return 0, 0, 0

        profit = 0
        accuracy = 0
        if label == predicted_label:
            accuracy = 1
            if label == 1:
                profit = match.B365H
            elif label == 0:
                profit = match.B365D
            else:
                profit = match.B365A
        return accuracy, 1, profit

    elif type_evaluation == 3:
        # best teams
        best_predicted_teams = predictor.get_best_team_predicted(match.get_league(), match.season, match.stage, n_teams_returned=6)

        if match.home_team_api_id in [t.team_api_id for t in best_predicted_teams]  \
                or match.away_team_api_id in [t.team_api_id for t in best_predicted_teams]:

            profit = 0
            accuracy = 0
            if label == predicted_label:
                accuracy = 1
                if label == 1:
                    profit = match.B365H
                elif label == 0:
                    profit = match.B365D
                else:
                    profit = match.B365A
            return accuracy, 1, profit
        else:
            return 0, 0, 0

    elif type_evaluation == 4:
        # 3 combined with 2
        best_predicted_teams = predictor.get_best_team_predicted(match.get_league(), match.season, match.stage, n_teams_returned=6)

        if match.home_team_api_id in [t.team_api_id for t in best_predicted_teams]  \
                or match.away_team_api_id in [t.team_api_id for t in best_predicted_teams]:

            if (predicted_label == 1 and prob < 1 / match.B365H) \
                    or (predicted_label == 0 and prob < 1 / match.B365D) \
                    or (predicted_label == 2 and prob < 1 / match.B365A):
                return 0, 0, 0

            profit = 0
            accuracy = 0
            if label == predicted_label:
                accuracy = 1
                if label == 1:
                    profit = match.B365H
                elif label == 0:
                    profit = match.B365D
                else:
                    profit = match.B365A
            return accuracy, 1, profit
        else:
            return 0, 0, 0

    elif type_evaluation == 5:
        # pick the bet with max probability and max odds 1.8
        if (predicted_label == 1 and (match.B365H > 1.8 or match.B365H < 1.6)) \
                or (predicted_label == 0 and (match.B365D > 1.8 or match.B365D < 1.6)) \
                or (predicted_label == 2 and (match.B365A > 1.8 or match.B365A < 1.6)):
            return 0, 0, 0

        if (predicted_label == 1 and prob < 1 / match.B365H) \
                or (predicted_label == 0 and prob < 1 / match.B365D) \
                or (predicted_label == 2 and prob < 1 / match.B365A):
            return 0, 0, 0

        profit = 0
        accuracy = 0
        if label == predicted_label:
            accuracy = 1
            if label == 1:
                profit = match.B365H
            elif label == 0:
                profit = match.B365D
            else:
                profit = match.B365A
        return accuracy, 1, profit

    elif type_evaluation == 6:

        profit = 0
        accuracy = 0
        if label == predicted_label:
            accuracy = 1
            if label == 1:
                profit = match.B365H
            elif label == 0:
                profit = match.B365D
            else:
                profit = match.B365A
        return accuracy, 1, profit
