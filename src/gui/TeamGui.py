import src.util.GuiUtil as GuiUtil
import src.application.Domain.Country as Country
import src.application.Domain.League as League
import src.application.Domain.Team as Team


def run():
    GuiUtil.print_head("Teams")
    menu = {1:"Country",2:"Name", 3:"League"}
    GuiUtil.print_menu("Find teams by:", menu, add_go_back = True)

    while True:
        try:
            user_input = input("\nSelect an item: ")
            user_input = int(user_input)

            if user_input==1:
                GuiUtil.print_info("Searching by", "country")
                search_by_country()

            elif user_input==2:
                GuiUtil.print_info("Searching by", "name")
                search_by_name()

            elif user_input==3:
                GuiUtil.print_info("Searching by", "league")
                search_by_league()

            else:
                raise ValueError

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Find teams by:", menu, add_go_back=True)

        except ValueError:
            if user_input == 'gb':
                return
            print("Insert a valid input!!!")


def search_by_country():
    user_input = input("Insert country name: ")
    countries = Country.read_by_name(user_input, like=True)

    if len(countries) == 0:
        GuiUtil.print_att("No country found", user_input)
    elif len(countries) == 1:
        country = countries[0]
        leagues = country.get_leagues()
        if len(leagues) == 0:
            GuiUtil.print_att("No leagues found in the country", country.name)
        else:
            teams = []
            for league in leagues:
                teams.extend(league.get_teams())
            if len(teams) == 0:
                GuiUtil.show_list_answer([], print_index=True)
            else:
                teams = sorted(teams, key=lambda team: team.team_long_name)
                teams_to_print = [t.team_long_name+": http://sofifa.com/team/"+str(t.team_fifa_api_id) for t in teams]
                GuiUtil.show_list_answer(teams_to_print, print_index=True)

def search_by_name():
    user_input = input("Insert team name: ")
    teams = Team.read_by_name(user_input, like=True)

    if len(teams) == 0:
        GuiUtil.print_att("No teams found", user_input)
    else:
        teams = sorted(teams, key=lambda team: team.team_long_name)
        teams_to_print = [t.team_long_name + ": http://sofifa.com/team/" + str(t.team_fifa_api_id) for t in teams]
        GuiUtil.show_list_answer(teams_to_print, print_index=True)


def search_by_league():
    user_input = input("Insert league name: ")
    leagues = League.read_by_name(user_input, like=True)

    if len(leagues) == 0:
        GuiUtil.print_att("No leagues found", user_input)
    elif len(leagues) == 1:
        teams = sorted(leagues[0].get_teams(), key=lambda team: team.team_long_name)
        teams_to_print = [t.team_long_name + ": http://sofifa.com/team/" + str(t.team_fifa_api_id) for t in teams]
        GuiUtil.show_list_answer(teams_to_print, print_index=True)
    else:
        GuiUtil.print_att("Too many leagues found", user_input)