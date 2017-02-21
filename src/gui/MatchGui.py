import src.util.GuiUtil as GuiUtil

import src.application.Domain.Team as Team
import src.application.Domain.Match as Match
import src.application.Domain.League as League
import src.util.util as util

def run():
    GuiUtil.print_head("Matches")
    menu = {1:"Find by Team",2:"Find by League", 3:"Find by Date"}
    GuiUtil.print_menu("Matches menu:", menu, add_go_back = True)

    while True:
        try:
            user_input = input("\nSelect an item: ")
            user_input = int(user_input)
            if user_input==1:
                GuiUtil.print_info("Searching by", "team")
                search_by_team()

            elif user_input==2:
                GuiUtil.print_info("Searching by", "league")
                search_by_league()

            elif user_input==3:
                GuiUtil.print_info("Searching by", "date")
                search_by_date()

            else:
                raise ValueError

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Matches Menu:", menu, add_go_back=True)

        except ValueError:
            if user_input == 'gb':
                return
            print("Insert a valid input!!!")


def search_by_date():
    date = GuiUtil.input_date_or_day_passed()
    matches = Match.read_by_match_date(date)
    matches = sorted(matches, key=lambda match: match.date)

    if len(matches) == 0:
        GuiUtil.print_att("No match found in date", date)
    else:
        for i, match in enumerate(matches):
            match_out = get_printable_match(match)
            GuiUtil.print_indent_answer(i + 1, match_out, True)


def search_by_team():
    user_input = input("Insert team name: ")
    GuiUtil.print_info("Looking for", user_input)
    teams_found = Team.read_by_name(user_input)

    GuiUtil.print_info("Teams found", len(teams_found))
    if len(teams_found) == 0:
        GuiUtil.print_att("Looking for team with similar name", user_input)
        teams_found = Team.read_by_name(user_input, like=True)

    if len(teams_found) == 0:
        GuiUtil.print_att("Teams found", 0)
    elif len(teams_found) == 1:
        team = teams_found[0]
        matches = team.get_matches(season=util.get_current_season(), ordered=True)
        for i, match in enumerate(matches):
            match_out = get_printable_match(match)
            GuiUtil.print_indent_answer(i + 1, match_out, True)
    else:
        GuiUtil.print_att("Too many teams found", "Be more precise")



def search_by_league():
    user_input = input("Insert league name: ")
    GuiUtil.print_info("Looking for", user_input)
    leagues = League.read_by_name(user_input, like=True)

    if len(leagues) == 0:
        GuiUtil.print_att("No leagues found with name", user_input)
    elif len(leagues) == 1:
        league = leagues[0]
        matches = league.get_matches(season=util.get_current_season(), ordered=True)
        for i, match in enumerate(matches):
            match_out = get_printable_match(match)
            GuiUtil.print_indent_answer(i + 1, match_out, True)


def get_printable_matches(matches):
    printable_matches = []
    for m in matches:
        printable_matches.append(get_printable_match(m))
    return printable_matches

def get_printable_match(match, show_event_link = False):
    league = League.read_by_id(match.league_id)
    match_str = league.name+" - Stage: "+str(match.stage) + " - "+match.date + "\n"

    home_team = match.get_home_team()
    away_team = match.get_away_team()

    # HOME TEAM INFO
    if home_team:
        match_str += home_team.team_long_name
    else:
        match_str += str(match.home_team_api_id)
    match_str += " " + str(match.home_team_goal)

    match_str += " vs "

    # AWAY TEAM INFO
    if away_team:
        match_str += away_team.team_long_name
    else:
        match_str += str(match.away_team_api_id)
    match_str += " " + str(match.away_team_goal)

    if not match.is_finished():
        match_str += " (TO BE CRAWLED)"

    # team formation home
    match_str += get_formation(match, home_team, home=True)
    # team formation away
    match_str += get_formation(match, away_team, home=False)

    if show_event_link:
        match_str += "\n(http://json.mx-api.enetscores.com/live_data/event/"+str(match.match_api_id)+"/0)"

    return match_str


def get_formation(match, team, home=True):

    formation_str = "\n\n" + team.team_short_name

    # get trends
    formation_str += get_team_trend_str(match, team)

    # get Goals
    formation_str += "\n"+get_team_goals_str(match, team)
    formation_str += "\n" + get_team_goals_str(match, team, n=5)

    if home:
        team_lines = match.get_home_team_lines_up()
    else:
        team_lines = match.get_away_team_lines_up()

    team_goal_done, team_goal_received, num_matches = team.get_goals_by_season_and_stage(util.get_current_season(), match.stage)


    for i, player in enumerate(team_lines):
        if not util.is_None(player):

            if player.is_gk():
                goal_dr = player.get_goal_received(season=util.get_current_season(), stage=match.stage)
                team_goal_dr = team_goal_received
            else:
                goal_dr = player.get_goal_done(season=util.get_current_season(), stage=match.stage)
                team_goal_dr = team_goal_done

            formation_str += '\n\t' + str(i + 1) + ") " + player.player_name.ljust(25, ".") \
                             + "\t P: "+str(len(player.get_matches(season=util.get_current_season(), stage=match.stage))) + '/' + str(match.stage-1) \
                             + "\t G: "+str(goal_dr)+"/"+str(team_goal_dr)

            if not player.is_gk():
                assist_done = player.get_assist_done(season=util.get_current_season(), stage=match.stage)
                team_assist_done = team.get_assist_by_season_and_stage(season=util.get_current_season(),
                                                                       stage=match.stage)
                formation_str += "\t A: " + str(assist_done) + "/" + str(team_assist_done)

    return formation_str


def get_team_goals_str(match, team, n=None):

    goal_done, goal_received, matches = team.get_goals_by_season_and_stage(season=match.season, stage=match.stage, n=n)
    home_goal_done, home_goal_received, home_matches = team.get_goals_by_season_and_stage(season=match.season, stage=match.stage, home=True, n=n)
    away_goal_done, away_goal_received, away_matches = team.get_goals_by_season_and_stage(season=match.season, stage=match.stage, home=False, n=n)

    team_goal_str = ""

    if matches > 0:
        team_goal_str += "\tG: "+str(round(goal_done/matches, 2))+" / "+str(round(goal_received/matches, 2))

    if home_matches > 0:
        team_goal_str += "\t\tHG: "+ str(round(home_goal_done / home_matches, 2)) + " / " + str(round(home_goal_received / home_matches, 2))

    if away_matches > 0:
        team_goal_str += "\t\tAG: "+ str(round(away_goal_done / away_matches, 2)) + " / " + str(round(away_goal_received / away_matches, 2))

    if team_goal_str != "":
        if n:
            team_goal_str = "(trend " + str(n) + ")" + team_goal_str
        else:
            team_goal_str = "(total)\t" + team_goal_str

    return team_goal_str


def get_team_trend_str(match, team):
    trend = team.get_trend(stage=match.stage, season=util.get_current_season())
    home_trend = team.get_trend(stage=match.stage, season=util.get_current_season(), home=True)
    away_trend = team.get_trend(stage=match.stage, season=util.get_current_season(), home=False)
    trend_str = ""
    if trend.strip() != "":
        trend_str += "\t\tT: " + trend
    if home_trend.strip() != "":
        trend_str += "\t\tHT: " + home_trend
    if away_trend.strip() != "":
        trend_str += "\t\tAT: " + away_trend

    return trend_str