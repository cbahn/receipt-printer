import json
import random
from escpos.printer import Usb

""" Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
p = Usb(0x0416, 0x5011)#, 0, profile="TM-T88III")



# Constant defining the maximum number of characters per line
LINE_MAX = 32

def random_value( d ):
    """ takes as input dictionary and returns a random value from amoungst all (key,value) pairs"""
    i =  random.randint(0, len(d))
    val = list(d.values())
    return val[i]


def pprint( s ):
    """ printer-print.
    This will eventually be modified so that it prints
    to the thermal receipt printer"""
    if len(s) > 32:
        raise ValueError("cannot print \"%s\", too long"%s)
    p.text(s + "\n")
    print(s)

def beautify_mana_cost( mc ):
    """ Takes a raw manacost string and removes the '{' and '}' characters to make it easier to read """
    return mc.translate(str.maketrans('','','{}'))

def name_cost_line_process(name,cost):
    """ takes in the raw cardname and manacost
    returns a LINE_MAX character string ready to be printed """
    pretty_mana_cost = beautify_mana_cost(cost)
    space_for_name = LINE_MAX - len(pretty_mana_cost) - 1
    name_format = '{:%d.%d}'%(space_for_name,space_for_name)
    return name_format.format(name) + ' ' + pretty_mana_cost

def cut_string_into_lines(s):
    """ this cuts a string into a list of strings,
    each of which are at most LINE_MAX characters.
    It also makes breaks at all '\n' newline characters """
    lines = s.split('\n')
    for l in lines:
        for start in range(0,len(l), LINE_MAX):
            yield l[start:start+LINE_MAX]

def cut_string_into_lines_spacebreak(s):
    """ Cuts a string into lines that are at most LINE_MAX characters,
    while only breaking lines as spaces"""
    lines = s.split('\n')
    for l in lines:
        words = l.split(' ')
        length = 0
        new_line = []
        for w in words:
            if length + 1 + len(w) <= LINE_MAX:
                new_line.append(w)
                length += 1 + len(w)
            else:
                yield " ".join(new_line)
                new_line = [w]
                length = len(w)
        yield " ".join(new_line)



def print_card( card ):
    """ This takes as input a card dictionary then formats and
    prints it out using the pprint() function"""

    # Print a blank line to clear the stuff, I guess
    pprint("   ")

    # Print the name and mana cost on one line
    pprint(name_cost_line_process(card['name'],card['manaCost']))

    # Line of '-' befor the rules text
    pprint( '*' * LINE_MAX )

    # Print out the rules text with word wrapping (not bothering to break at spaces)
    if card['text'] != "":
        rules_text_lines = cut_string_into_lines_spacebreak( card['text'] )
        for p in rules_text_lines:
            pprint( p )

        # Put a line of '-' before P/T
        pprint( ' ' * LINE_MAX)

    # Print power and toughness right justified
    p_t_string = "%s / %s"%(card['power'],card['toughness'] )
    pprint( p_t_string.rjust(LINE_MAX) )


################################################

with open('output/ncards.json', encoding='utf8') as f:
    cards = json.load(f)





user_input = input("Enter creature CMC: ")
card = random_value(cards["%d"%int(user_input)])
print()
print_card(card)
p.cut()