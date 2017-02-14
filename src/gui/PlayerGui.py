import src.util.GuiUtil as GuiUtil
import src.application.Domain.Player as Player
import src.application.Domain.Team as Team

def run():
    GuiUtil.print_head("Players")
    menu = {1:"Name",2:"Team"}
    GuiUtil.print_menu("Find player by:", menu, add_go_back = True)

    while True:
        try:
            user_input = input("\nSelect an item: ")
            user_input = int(user_input)
            if user_input==1:
                GuiUtil.print_info("Searching by", "name")
                search_by_name()

            elif user_input==2:
                GuiUtil.print_info("Searching by", "team")
                search_by_team()

            else:
                raise ValueError

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Find player by:", menu, add_go_back=True)

        except ValueError:
            if user_input == 'gb':
                return
            print("Insert a valid input!!!")


def search_by_name():
    user_input = input("Insert a name: ")
    GuiUtil.print_info("Looking for", user_input)
    players_found = Player.read_by_name(user_input)
    GuiUtil.print_info("Players found", len(players_found))
    if len(players_found) == 0:
        GuiUtil.print_info("Looking for player with similar name", user_input)
        players_found = Player.read_by_name(user_input, like=True)

    GuiUtil.show_list_answer(players_found)


def search_by_team():
    user_input = input("Insert team name: ")
    GuiUtil.print_info("Looking for", user_input)
    teams_found = Team.read_by_name(user_input)

    if len(teams_found) == 0:
        GuiUtil.print_att("No team found with name", user_input)
    elif len(teams_found) == 1:
        team = teams_found[0]
        GuiUtil.show_list_answer(team.get_current_players())

