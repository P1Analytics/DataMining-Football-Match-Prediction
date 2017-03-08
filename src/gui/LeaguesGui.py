import src.util.GuiUtil as GuiUtil
import src.util.util as util
import src.application.Domain.Country as Country
import src.application.Domain.League as League


def run():
    GuiUtil.print_head("Leagues")
    menu = {1:"Country",2:"Name"}
    GuiUtil.print_menu("Find leagues by:", menu, add_go_back = True)

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

            else:
                raise ValueError

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Find leagues by:", menu, add_go_back=True)

        except ValueError:
            if user_input == 'gb':
                return
            print("Insert a valid input!!!")


def search_by_country():
    user_input = input("Insert country name: ")
    countries = Country.read_by_name(user_input, like=False)

    if len(countries) == 0:
        GuiUtil.print_att("No country found with correct name", user_input)
        GuiUtil.print_info("Searching for coutnry with similar name", user_input)
        countries = Country.read_by_name(user_input, like=True)

    if len(countries) == 1:
        country = countries[0]
        leagues = country.get_leagues()
        if len(leagues) == 0:
            GuiUtil.print_att("No leagues found in the country", country.name)
        else:
            GuiUtil.show_list_answer([get_league_str(league) for league in leagues], print_index=True, label="League by country", label_value=user_input)
    else:
        for country in countries:
            leagues = country.get_leagues()
            if len(leagues) == 0:
                GuiUtil.print_att("No leagues found in the country", country.name)
            else:
                GuiUtil.show_list_answer([get_league_str(league) for league in leagues], print_index=True,
                                         label="League by country", label_value=country.name)


def search_by_name():
    user_input = input("Insert league name: ")
    leagues = League.read_by_name(user_input, like=True)

    if len(leagues) == 0:
        GuiUtil.print_att("No Leagues found", user_input)
    else:
        GuiUtil.show_list_answer([get_league_str(league) for league in leagues], print_index=True, label="League by name", label_value=user_input)


def get_league_str(league):
    league_str = league.name

    # ranking
    league_str += "\nRanking:"
    ranking = league.get_ranking(util.get_current_season())
    league_str = get_ramking_str(ranking)

    # home rankig
    # TODO HOME RANKING
    '''
    league_str += "\nHome Ranking:"
    ranking = league.get_ranking(util.get_current_season(), home=True)
    league_str = get_ramking_str(ranking)
    '''


    return league_str


def get_ramking_str(ranking):
    ranking_str = ""
    i = 1
    for points, team in ranking:
        ranking_str += ("\n\t" + str(i) + ") " + team.team_long_name).ljust(50, '.') + " " + str(points)
        i += 1
    return ranking_str


