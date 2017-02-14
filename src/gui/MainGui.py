import src.gui.PlayerGui as PlayerGui
import src.gui.MatchGui as MatchGui
import src.util.GuiUtil as GuiUtil

def run():
    head = "ScorePrediction application"
    GuiUtil.print_head(head)
    menu = {1:"Players", 2:"Matches", 3:"Leagues", 4:"Countries", 5:"Teams"}
    GuiUtil.print_menu("Browse the application to discover different data", menu)

    while True:
        try:
            user_input = input("\nSelect an item: ")
            user_input = int(user_input)
            if user_input==1:
                GuiUtil.print_info("Opening", "Players")
                PlayerGui.run()
                GuiUtil.print_head(head)

            elif user_input==2:
                GuiUtil.print_info("Opening", "Mathces")
                MatchGui.run()
                GuiUtil.print_head(head)

            elif user_input == 3:
                GuiUtil.print_info("Opening", "Leagues")

            elif user_input == 4:
                GuiUtil.print_info("Opening", "Countries")

            elif user_input == 5:
                GuiUtil.print_info("Opening", "Teams")

            GuiUtil.print_menu("Browse the application to discover different data", menu)
        except ValueError:
            print("Insert a valid input!!!")

