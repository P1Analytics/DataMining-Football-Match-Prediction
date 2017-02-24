def kekko_input(domain,
              representation,
              stage_to_predict,         # number of next stage we want to predict
              season,
              stages_to_train=None,     # numebr of stages to consider
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

    # totale + casa
    # totale + trasferta

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

        # last 5 matches,
        # last 5 matches home,
        # last 5 matches away
        home_trend = home_team.get_trend(stage=match.stage, season=match.season).replace("P", "2").replace("V","1").replace("X", "0")
        home_home_trend = home_team.get_trend(stage=match.stage, season=match.season, home=True).replace("P", "2").replace("V","1").replace("X", "0")
        home_away_trend = home_team.get_trend(stage=match.stage, season=season, home=False).replace("P", "2").replace("V","1").replace("X", "0")

        away_trend = away_team.get_trend(stage=match.stage, season=match.season).replace("P", "2").replace("V", "1").replace("X", "0")
        away_home_trend = away_team.get_trend(stage=match.stage, season=match.season, home=True).replace("P", "2").replace("V", "1").replace("X", "0")
        away_away_trend = away_team.get_trend(stage=match.stage, season=season, home=False).replace("P", "2").replace("V", "1").replace("X", "0")

        try:
            home_in = home_trend.split().extend(home_home_trend.split()).extend(home_away_trend.split())
            away_in = away_trend.split().extend(away_home_trend.split()).extend(away_away_trend.split())
        except AttributeError:
            continue
        if len(home_in)!=15 and len(away_in)!=15:
            continue
        print(home_in, away_in)
        matches.append(home_in.extend(away_in))
        matches_names.append(home_team.team_long_name + " vs " + away_team.team_long_name)

        if match.home_team_goal > match.away_team_goal:
            labels.append(1)
        elif match.home_team_goal < match.away_team_goal:
            labels.append(2)
        else:
            labels.append(0)




    pass
