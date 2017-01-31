pad_len = 50

def print_head(head):
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