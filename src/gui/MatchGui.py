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

    if len(matches) == 0:
        GuiUtil.print_att("No match found in date", date)
    else:
        printable_matches = get_printable_matches(matches)
        GuiUtil.show_list_answer(printable_matches, print_index=True)



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
        printable_matches = get_printable_matches(matches)
        GuiUtil.show_list_answer(printable_matches, print_index=False)
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
        printable_matches = get_printable_matches(matches)
        GuiUtil.show_list_answer(printable_matches, print_index=False)

def get_printable_matches(matches):
    printable_matches = []
    for m in matches:
        printable_matches.append(get_printable_match(m))
    return printable_matches

def get_printable_match(match, show_event_link = False):
    match_str = "Stage: "+str(match.stage) + " "+match.date + " "
    home_team = match.get_home_team()
    away_team = match.get_away_team()

    if home_team:
        match_str += home_team.team_long_name
    else:
        match_str += str(match.home_team_api_id)
    match_str += " " + str(match.home_team_goal) + " vs "

    if away_team:
        match_str += away_team.team_long_name
    else:
        match_str += str(match.away_team_api_id)
    match_str += " " + str(match.away_team_goal)

    if show_event_link:
        match_str += " (http://json.mx-api.enetscores.com/live_data/event/"+str(match.match_api_id)+"/0)"

    return match_str

