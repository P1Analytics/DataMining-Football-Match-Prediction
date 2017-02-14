import src.util.GuiUtil as GuiUtil
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
    countries = Country.read_by_name(user_input, like=True)

    if len(countries) == 0:
        GuiUtil.print_att("No country found", user_input)
    elif len(countries) == 1:
        country = countries[0]
        leagues = country.get_leagues()
        if len(leagues) == 0:
            GuiUtil.print_att("No leagues found in the country", country.name)
        else:
            GuiUtil.show_list_answer([league.name for league in leagues], print_index=True)


def search_by_name():
    user_input = input("Insert league name: ")
    leagues = League.read_by_name(user_input, like=True)

    if len(leagues) == 0:
        GuiUtil.print_att("No Leagues found", user_input)
    else:
        GuiUtil.show_list_answer([league.name for league in leagues], print_index=True)



