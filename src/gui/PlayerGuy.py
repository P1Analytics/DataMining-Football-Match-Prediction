import src.util.GuiUtil as GuiUtil

def run():
    GuiUtil.print_head("Players")

    print("Find player by:")
    print("\t1 Name")
    print("\t2 Team")
    print("\t3 Country")
    print("\tgb to go back")

    while True:
        try:
            user_input = input("\nSelect an item:")
            user_input = int(user_input)
            if user_input==1:
                print("Searching by name...")

            elif user_input==2:
                print("Searching by team...")

            elif user_input == 3:
                print("Searching by country...")

        except ValueError:
            if user_input == "gb":
                return
            else:
                print("Insert a valid input!!!")