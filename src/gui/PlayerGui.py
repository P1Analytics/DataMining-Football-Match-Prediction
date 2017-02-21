import src.util.GuiUtil as GuiUtil
import src.application.Domain.Player as Player
import src.application.Domain.Team as Team
import src.util.util as util


def run():
    GuiUtil.print_head("Players")
    menu = {1: "Find by Name", 2: "Find by Team"}
    GuiUtil.print_menu("Players menu:", menu, add_go_back=True)

    while True:
        try:
            user_input = input("\nSelect an item: ")
            user_input = int(user_input)
            if user_input == 1:
                GuiUtil.print_info("Searching by", "name")
                search_by_name()

            elif user_input == 2:
                GuiUtil.print_info("Searching by", "team")
                search_by_team()

            else:
                raise ValueError

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Players menu:", menu, add_go_back=True)

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

    if len(players_found) == 1:
        show_players(players_found[0].player_name, players_found, "Players by exact name")
    else:
        show_players(user_input, players_found, "Players by similar name")


def search_by_team():
    user_input = input("Insert team name: ")
    GuiUtil.print_info("Looking for", user_input)

    teams_found = Team.read_by_name(user_input, like=False)
    if len(teams_found) == 0:
        GuiUtil.print_att("No team found with exact name", user_input)
        teams_found = Team.read_by_name(user_input, like=True)
        if len(teams_found) == 0:
            GuiUtil.print_att("No team found", user_input)
        elif len(teams_found) == 1:
            team = teams_found[0]
            show_players(user_input, team.get_current_players(), "Players of the team", team=team, show_details=True)

    elif len(teams_found) == 1:
        team = teams_found[0]
        show_players(user_input, team.get_current_players(), "Players of the team", team=team, show_details=True)


def show_players(user_input, players_in, label, team=None, show_details=False):
    players_in = sorted(players_in, key=lambda player: player.player_name)
    print("[ANSWER of " + label + " --> " + str(user_input) + "]")

    show_details = len(players_in) < 10 or show_details
    for i, player_in in enumerate(players_in):
        player_out = get_player_str(player_in, show_details, team)
        GuiUtil.print_indent_answer(i+1, player_out, True)


def get_player_str(player, show_details, current_player_team=None):
    player_link = "http://sofifa.com/player/"
    player_str = player.player_name + " " + player_link + str(player.player_fifa_api_id)

    if show_details:
        if not current_player_team:
            current_player_team = player.get_current_team()
        if current_player_team:
            # current team
            player_str += '\nCurrent team: ' + current_player_team.team_long_name

            # matches played
            team_matches = current_player_team.get_matches(season=util.get_current_season())
            player_str += '\nGames when he starts from the beginning: ' \
                          + str(len(player.get_matches(season=util.get_current_season()))) + '/' \
                          + str(len(team_matches))

            # goals done / received
            team_goal_done, team_goal_received = current_player_team.get_goals_by_season(
                season=util.get_current_season())
            if not player.is_gk():
                goal_done = player.get_goal_done(season=util.get_current_season())
                player_str += '\nGoal done: ' + str(goal_done) + "/" + str(team_goal_done)

                # assist done
                assist_done = player.get_assist_done(season=util.get_current_season())
                team_assist_done = current_player_team.get_assist_by_season_and_stage(season=util.get_current_season())
                player_str += '\nAssist done: ' + str(assist_done) + "/" + str(team_assist_done)
            else:
                goal_recived = player.get_goal_received(season=util.get_current_season())
                player_str += '\nGoal Received: ' + str(goal_recived) + "/" + str(team_goal_received)

        else:
            # current team not found
            player_str += '\nCurrent team: NOT FOUND'

            # matches played
            player_str += '\nGames when he starts from the beginning: ' \
                          + str(len(player.get_matches(season=util.get_current_season())))

            # goals done / received
            if not player.is_gk():
                goal_done = player.get_goal_done(season=util.get_current_season())
                player_str += '\nGoal done: ' + str(goal_done)

                # assist done
                assist_done = player.get_assist_done(season=util.get_current_season())
                player_str += '\nAssist done: ' + str(assist_done)
            else:
                goal_recived = player.get_goal_received(season=util.get_current_season())
                player_str += '\nGoal Received: ' + str(goal_recived)

    return player_str


