import src.gui.PlayerGuy as PlayerGuy
import src.util.GuiUtil as GuiUtil

def run():
    GuiUtil.print_head("Welcome to ScorePrediction application")
    menu = {1:"Players", 2:"Matches", 3:"Leagues", 4:"Countries", 5:"Teams"}
    GuiUtil.print_menu("Browse the application to discover different data", menu)

    while True:
        try:
            user_input = input("\nSelect an item:")
            user_input = int(user_input)
            if user_input==1:
                print("Opening Players...")
                PlayerGuy.run()
            elif user_input==2:
                print("Opening Matches...")

            elif user_input == 3:
                print("Opening Leagues...")

            elif user_input == 4:
                print("Opening Countries...")

            elif user_input == 5:
                print("Opening Teams...")

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Browse the application to discover different data", menu)
        except ValueError:
            print("Insert a valid input!!!")

