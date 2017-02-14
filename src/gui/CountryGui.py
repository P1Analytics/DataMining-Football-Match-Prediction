import src.util.GuiUtil as GuiUtil

import src.application.Domain.Country as Country

def run():
    GuiUtil.print_head("Countries")
    menu = {1:"Name"}
    GuiUtil.print_menu("Country menu:", menu, add_go_back = True)

    while True:
        try:
            user_input = input("\nSelect an item: ")
            user_input = int(user_input)

            if user_input==1:
                GuiUtil.print_info("Searching by", "country")
                search_by_name()

            else:
                raise ValueError

            GuiUtil.print_line_separator()
            GuiUtil.print_menu("Country Menu:", menu, add_go_back=True)

        except ValueError:
            if user_input == 'gb':
                return
            print("Insert a valid input!!!")


def search_by_name():
    user_input = input("Insert country name: ")
    countries = Country.read_by_name(user_input, like=True)

    if len(countries) == 0:
        GuiUtil.print_att("No country found", user_input)
    else:
        GuiUtil.show_list_answer([c.name for c in countries], print_index=True)