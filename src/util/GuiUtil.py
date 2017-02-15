import src.util.util as util

pad_len = 100

def print_head(head):
    print()
    print("".ljust(pad_len,'*'))
    head_pad = int((pad_len - len(head) - 2)/2)
    print("".ljust(head_pad,'*')+" "+head+" "+"".ljust(head_pad,'*'))
    print("".ljust(pad_len, '*'))

def print_line_separator():
    print("".ljust(pad_len, '*'))

def print_menu(text, choices, add_go_back=False):
    print(text)
    for k,v in choices.items():
        print("\t-",k,":",v)
    if add_go_back:
        print("\t- gb : Go back")

def print_info(label, user_input):
    print("[INFO: "+label+" --> "+str(user_input)+"]")

def show_list_answer(l, print_index=True):
    if len(l)>0:
        print ("[ANSWER]")
        print_ans = 1
        if len(l) > 20:
            print_ans = print_att("Too many rows to print", len(l), check_continue=True)

        if print_ans == 1:
            for i, answer in enumerate(l):
                answer_str = answer.__str__()
                print_indent_answer(i+1, answer_str, print_index)

def print_indent_answer(i, answer_str, print_index):

    answer_line_len = int(pad_len*3/4)
    if print_index:
        print("\t" + str(i) + ") " + answer_str[0 : answer_line_len+1])
    else:
        print("\t" + answer_str[0: answer_line_len + 1])

    line = 1
    while len(answer_str) >= line * answer_line_len:
        print("\t\t" + answer_str[line * answer_line_len +1: (line + 1) * answer_line_len+1])
        line += 1


def print_att(label, value, check_continue=False):
    print("[ATT: "+label+" --> "+str(value)+"]")
    if check_continue:
        print_menu("Do you want to continue?", {'n':"False", "<enter>":"True"})
        user_input = input("Type: ")
        if user_input == 'n' or user_input == 'N':
            return 0

    return 1


def print_err(label, value):
    print("[ERR: "+label+" --> "+str(value)+"]")


def input_date_or_day_passed(retry_on_error=True):
    user_input = input("Insert a date (YYYY-MM-DD) or an integer (the day passed from today --> 0 is today): ")
    while True:
        try:
            day_passed = int(user_input)
            date = util.get_date(day_passed)
        except ValueError:
            date = util.get_date_by_string(user_input)

        if date or not retry_on_error:
            return date

        user_input = input("Insert a valid value: ")
