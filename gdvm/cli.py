from collections import namedtuple
from colorama import Fore, Style
from sys import exit

from .helpers import abort




def item_repr(item: str, number=None, padding=False, selected=False) -> str:
    numbering = ''
    if number is not None:
        numbering = f'[{number}]\t'

    prefix = ''
    if padding:
        prefix = '   '
    if selected:
        prefix = '-> '
    return f'{prefix}{numbering}{item}'



Choice = namedtuple('Choice', 'id display')

def _display_choice(displays: list[str],
                    default_item:str='') -> list[Choice]:
    """Display a list of choices with an associated number

       Return a Choice(id,display) named tuple
    """
    choices = [Choice(id,display)
               for id, display in enumerate(displays)]

    for choice in choices:
        repr = item_repr(choice.display,
                         padding=(True if default_item else False),
                         selected=(choice.display==default_item),
                         number=choice.id)
        print(repr)

    return choices



def pick(items: list[str], default_item:str='') -> str:
    """ Pick from a list of displayed strings

        Return the selected choice
    """
    if len(items) == 0:
        print('Interactive picker error: no item to pick from')
        abort()

    # print versions with an associated number
    choices = _display_choice(items, default_item)

    if not default_item:
        return pick_choice(choices).display or ''

    for c in choices:
        if c.display == default_item:
            return pick_choice(choices, default=c).display


def pick_choice(choices: list[Choice], default:Choice|None=None) -> Choice:
    default_str = f' (default={default.id})' if default else ''

    # ask which number to use
    try:
        usr_input = input(f'Enter the choosen number{default_str}: ')
    except KeyboardInterrupt:
        print() # print on new line
        exit()

    if not usr_input:
        if not default:
            print('No item selected')
            exit()
        return default

    try:
        chosen_number = int(usr_input)
    except ValueError:
        print('Incorrect input')
        abort()

    if not 0 <= chosen_number < len(choices):
        print('Incorrect number')
        abort()

    return choices[chosen_number]
