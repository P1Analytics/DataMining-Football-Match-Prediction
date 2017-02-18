import src.util.GuiUtil as GuiUtil

def run():
    GuiUtil.print_head("Bet odds")
    menu = {1: "All bet odds of today"}
    GuiUtil.print_menu("Bet odds menu:", menu, add_go_back=True)
