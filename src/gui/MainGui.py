import src.gui.PlayerGui as PlayerGui
import src.gui.MatchGui as MatchGui
import src.gui.LeaguesGui as LeaguesGui
import src.gui.CountryGui as CountryGui
import src.gui.TeamGui as TeamGui
import src.gui.CrawlGui as CrawlGui
import src.util.GuiUtil as GuiUtil

def run():
    head = "ScorePrediction application"
    GuiUtil.print_head(head)
    menu = {1:"Players", 2:"Matches", 3:"Leagues", 4:"Countries", 5:"Teams", 6:"Crawling"}
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
                LeaguesGui.run()
                GuiUtil.print_head(head)

            elif user_input == 4:
                GuiUtil.print_info("Opening", "Countries")
                CountryGui.run()
                GuiUtil.print_head(head)

            elif user_input == 5:
                GuiUtil.print_info("Opening", "Teams")
                TeamGui.run()
                GuiUtil.print_head(head)

            elif user_input == 6:
                GuiUtil.print_info("Opening", "Crawling")
                CrawlGui.run()
                GuiUtil.print_head(head)

            GuiUtil.print_menu("Browse the application to discover different data", menu)
        except ValueError:
            print("Insert a valid input!!!")

