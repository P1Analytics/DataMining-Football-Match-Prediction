import src.util.GuiUtil as GuiUtil

import src.application.Domain.Team as Team
import src.application.Domain.Match as Match
import src.application.Domain.League as League
import src.util.util as util

def run():
    GuiUtil.print_head("Match")
    menu = {1:"Team",2:"League", 3:"Date"}
    GuiUtil.print_menu("Find match by:", menu, add_go_back = True)

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
            GuiUtil.print_menu("Find matches by:", menu, add_go_back=True)

        except ValueError:
            if user_input == 'gb':
                return
            print("Insert a valid input!!!")


def search_by_date():
    date = GuiUtil.input_date_or_day_passed()
    print(date)



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
        printable_matches = []
        for m in matches:
            printable_matches.append(get_printable_match(m))

        GuiUtil.show_list_answer(printable_matches, print_index=False)


def search_by_league():
    user_input = input("Insert league name: ")
    GuiUtil.print_info("Looking for", user_input)
    leagues = League.read_by_name(user_input, like=True)

    if len(leagues) == 0:
        GuiUtil.print_att("No leagues found with name", user_input)
    elif len(leagues) == 1:
        league = leagues[0]
        matches = league.get_matches(season=util.get_current_season(), ordered=True)
        printable_matches = []
        for m in matches:
            printable_matches.append(get_printable_match(m))

        GuiUtil.show_list_answer(printable_matches, print_index=False)


def get_printable_match(match):
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

    return match_str

