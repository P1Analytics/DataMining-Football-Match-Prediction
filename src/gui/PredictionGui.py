import src.util.GuiUtil as GuiUtil

def run():
    GuiUtil.print_head("Predictions")
    menu = {1: "Predict matches"}
    GuiUtil.print_menu("Predictions menu:", menu, add_go_back=True)