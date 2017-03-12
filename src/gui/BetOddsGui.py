import src.util.util as util
import src.util.GuiUtil as GuiUtil
import src.application.Domain.Match as Match
import src.application.Domain.MatchEvent as MatchEvent

def run():
    GuiUtil.print_head("Bet odds")
    menu = {1: "All bet-odds of today", 2: "Bet-odds by date"}
    GuiUtil.print_menu("Bet odds menu:", menu, add_go_back=True)

    while True:
        try:
            user_input = input("\nSelect an item: ")
            user_input = int(user_input)
            if user_input==1:
                GuiUtil.print_info("Bet odds", "today")
                print_bet_odds(util.get_today_date(with_hours=False))

            elif user_input==2:
                GuiUtil.print_info("Bet odds", "by date")
                print_bet_odds(GuiUtil.input_date_or_day_passed())

            else:
                raise ValueError

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Bet odds Menu:", menu, add_go_back=True)

        except ValueError:
            if user_input == 'gb':
                return
            print("Insert a valid input!!!")


def print_bet_odds(date):
    GuiUtil.print_info("Bet odds of", date)
    matches = Match.read_by_match_date(date, order_by_date=True)
    pi = 1
    for match in matches:
        match_event_out = get_match_event_out(match)
        GuiUtil.print_indent_answer(pi, match_event_out, True)
        pi += 1

    if pi == 1:
        GuiUtil.print_att("No match found", date)


def get_bet_event_out(bet_event):
    bet_event_str = "\n\n\t-" + bet_event.event_name+":"
    for bet_name, bet_odds in bet_event.get_bet_odds().items():
        bet_event_str += "\n\t| "+bet_name+":\t"+str(bet_odds)

    return bet_event_str


def get_match_event_out(match):
    match_event_str = ""

    match_event_str += match.get_home_team().team_long_name + " vs " + match.get_away_team().team_long_name
    match_event_str += "\n"+"["+match.date+"]"

    match_event = match.get_match_event()
    if util.is_None(match_event):
        match_event_str += "\nNo bet-odds found"
        return match_event_str

    bet_events_dict = match_event.get_last_bet_values()

    for bet_event_name, bet_event in bet_events_dict.items():
        match_event_str += get_bet_event_out(bet_event)

    return match_event_str
