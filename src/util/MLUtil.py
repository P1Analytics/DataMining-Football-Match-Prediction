def get_label(match):
    if match.home_team_goal > match.away_team_goal:
        return 1
    elif match.home_team_goal < match.away_team_goal:
        return 2
    else:
        return 0