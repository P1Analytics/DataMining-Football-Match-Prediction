import numpy as np

from src.application.Exception.MLException import MLException


def kekko_input(domain,
              representation,
              stage_to_predict,         # number of next stage we want to predict
              season,
              stages_to_train=90,     # numebr of stages to consider
                                        # --> it define the size of the train (EX: 38 * 10 train input)
              ):

    # [last 5 matches,
    # last 5 matches home,
    # last 5 matches away,
    # goal totali FATTI
    # goal totali SUBITI
    # goal fatti in casa,
    # goal subiti in casa,
    # goal fatti in trasferta
    # goal subiti in trasferta
    # posizione in classifica
    # posizione in classifica casa
    # posizione in classifica trasferta]

    matches = []
    matches_to_predict = []
    labels = []
    labels_to_predict = []
    matches_names = []
    matches_to_predict_names = []

    training_matches = domain.get_training_matches(season, stage_to_predict, stages_to_train)

    for match in training_matches:
        home_team = match.get_home_team()
        away_team = match.get_away_team()
        try:
            # posizione in classifica
            # posizione in classifica casa
            # posizione in classifica trasferta]
            match_as_array = [get_classifica(domain, home_team, match.season, match.stage, stages_to_train)]
            #match_as_array.extend([get_classifica(domain, home_team, match.season, match.stage, stages_to_train, home=True)])
            #match_as_array.extend([get_classifica(domain, home_team, match.season, match.stage, stages_to_train, home=False)])
            match_as_array.extend([get_classifica(domain, away_team, match.season, match.stage, stages_to_train)])
            #match_as_array.extend([get_classifica(domain, away_team, match.season, match.stage, stages_to_train, home=True)])
            #match_as_array.extend([get_classifica(domain, away_team, match.season, match.stage, stages_to_train, home=False)])

            # last 5 matches, last 5 matches home, last 5 matches away
            home_trend = get_trend(home_team, match.stage, match.season)
            away_trend = get_trend(away_team, match.stage, match.season)
            if len(home_trend) != 5 or len(away_trend) != 5:
                continue

            match_as_array.extend(home_trend)
            match_as_array.extend(away_trend)

            # goal totali FATTI, goal totali SUBITI, goal fatti in casa, goal subiti in casa, goal fatti in trasferta, goal subiti in trasferta
            match_as_array.extend(get_goals(home_team, match.stage, match.season, stages_to_train))
            #match_as_array.extend(get_goals(home_team, match.stage, match.season, stages_to_train//2, home=True))
            #match_as_array.extend(get_goals(home_team, match.stage, match.season, stages_to_train//2, home=False))
            match_as_array.extend(get_goals(away_team, match.stage, match.season, stages_to_train))
            #match_as_array.extend(get_goals(away_team, match.stage, match.season, stages_to_train//2, home=True))
            #match_as_array.extend(get_goals(away_team, match.stage, match.season, stages_to_train//2, home=False))

            matches.append(np.asarray(match_as_array))
            matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)
            labels.append(get_label(match))

        except MLException:
            continue

    for match in [m for m in domain.get_matches(season=season) if m.stage == stage_to_predict]:
        home_team = match.get_home_team()
        away_team = match.get_away_team()

        try:
            match_as_array = [get_classifica(domain, home_team, match.season, match.stage, stages_to_train)]
            #match_as_array.extend([get_classifica(domain, home_team, match.season, match.stage, stages_to_train, home=True)])
            #match_as_array.extend([get_classifica(domain, home_team, match.season, match.stage, stages_to_train, home=False)])
            match_as_array.extend([get_classifica(domain, away_team, match.season, match.stage, stages_to_train)])
            #match_as_array.extend([get_classifica(domain, away_team, match.season, match.stage, stages_to_train, home=True)])
            #match_as_array.extend([get_classifica(domain, away_team, match.season, match.stage, stages_to_train, home=False)])

            home_trend = get_trend(home_team, match.stage, match.season)
            away_trend = get_trend(away_team, match.stage, match.season)
            if len(home_trend) != 5 or len(away_trend) != 5:
                continue

            match_as_array.extend(home_trend)
            match_as_array.extend(away_trend)

            # goal totali FATTI, goal totali SUBITI, goal fatti in casa, goal subiti in casa, goal fatti in trasferta, goal subiti in trasferta
            match_as_array.extend(get_goals(home_team, match.stage, match.season, stages_to_train))
            #match_as_array.extend(get_goals(home_team, match.stage, match.season, stages_to_train//2, home=True))
            #match_as_array.extend(get_goals(home_team, match.stage, match.season, stages_to_train//2, home=False))
            match_as_array.extend(get_goals(away_team, match.stage, match.season, stages_to_train))
            #match_as_array.extend(get_goals(away_team, match.stage, match.season, stages_to_train//2, home=True))
            #match_as_array.extend(get_goals(away_team, match.stage, match.season, stages_to_train//2, home=False))

            matches_to_predict.append(np.asarray(match_as_array))

            labels_to_predict.append(get_label(match))
            matches_to_predict_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

        except MLException:
            continue

    matches = np.asarray(matches)
    matches_to_predict = np.asarray(matches_to_predict)
    labels = np.asarray(labels)
    labels_to_predict = np.asarray(labels_to_predict)

    if len(matches) == 0 or len(matches_to_predict) == 0:
        raise MLException(2)

    return matches, labels, matches_names, matches_to_predict, matches_to_predict_names, labels_to_predict


def get_label(match):
    if match.home_team_goal > match.away_team_goal:
        return 1
    elif match.home_team_goal < match.away_team_goal:
        return 2
    else:
        return 0


def get_goals(team, match_stage, match_season, stages_to_train, home=None):
    goal_done, goal_received, n = team.get_goals_by_train_matches(match_season, match_stage, stages_to_train, home=home)

    return [goal_done/n, goal_received/n]


def get_trend(team, match_stage, match_season):
    trend = []
    trend.extend(transform_tren(team.get_trend(stage=match_stage, season=match_season)))
    #trend.extend(transform_tren(team.get_trend(stage=match_stage, season=match_season, home=True)))
    #trend.extend(transform_tren(team.get_trend(stage=match_stage, season=match_season, home=False)))

    return trend


def transform_tren(trend_str):
    trend_list = []
    point = 0
    for t in trend_str.split():
        if t == 'V':
            # win
            trend_list.append(1)
            point += 3
        elif t == 'P':
            # lost
            trend_list.append(2)
        elif t == 'X':
            # draw
            trend_list.append(0)
            point += 1

    return trend_list
    #return [point]

def get_classifica(league, team, season, stage_to_predict, stages_to_train, home=None):
    pos = 1
    #for points_i, team_i in league.get_training_ranking(season, stage_to_predict, stages_to_train, home=home):
    for points_i, team_i in league.get_ranking(season, stages_to_train-1, home=home):
        if team.id == team_i.id:
            return pos
        pos += 1

    return pos