import src.util.GuiUtil as GuiUtil
import src.application.Crawl.enetscores.Crawler as CrawlerMatches
import src.application.Crawl.sofifa.Crawler as CrawlerPlayers

def run():
    GuiUtil.print_head("Crawling")
    menu = {1: "Find new matches", 2: "Find new players"}
    GuiUtil.print_menu("Crawl menu:", menu, add_go_back=True)

    while True:
        try:
            user_input = input("\nSelect an item: ")
            user_input = int(user_input)
            if user_input == 1:
                GuiUtil.print_info("Finding", "matches")
                find_new_matches()

            elif user_input == 2:
                GuiUtil.print_info("Finding", "players")
                find_new_players()

            else:
                raise ValueError

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Crawl Menu:", menu, add_go_back=True)

        except ValueError:
            if user_input == 'gb':
                return
            print("Insert a valid input!!!")

def find_new_matches():
    print("Type the last day to be crawled")
    starting_date = GuiUtil.input_date_or_day_passed()

    while True:
        try:
            user_input = input("Insert number of days back to date (if 0 --> only the date) to be crawled: ")
            stop_when = int(user_input)
            break
        except ValueError:
            GuiUtil.print_err("Value error", user_input)

    go_back = stop_when != 0
    CrawlerMatches.start_crawling(go_back, stop_when, starting_date)


def find_new_players():
    CrawlerPlayers.start_crawling()

