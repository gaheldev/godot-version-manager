from collections import namedtuple
from colorama import Fore, Style

from .helpers import abort




def _selection_display(item: str, default_item:str='') -> str:
    if not default_item:
        return ''

    if default_item == item:
        return '-> '
    else:
        return '   '


def _use_display(item: str, system:str='', local:str='') -> str:
    suffix = ''
    if item == system:
        suffix += f'{Fore.RED} System'
    if item == local:
        suffix += f'{Fore.YELLOW} Local'
    return suffix



def _verbose_display(item: str, system:str='', local:str='') -> str:
    default_item = ''
    if local:
        default_item = local
    elif system:
        default_item = system

    suffix = _use_display(item, system, local)

    return f'{_selection_display(item, default_item)}{item}{suffix}{Style.RESET_ALL}'



Choice = namedtuple('Choice', 'id display')

def _display_choice(displays: list[str], default_item:str='') -> list[Choice]:
    """Display a list of choices with an associated number

       Return a Choice(id,display) named tuple
    """
    choices = [Choice(id,display)
               for id, display in enumerate(displays)]

    to_display = [f'{_selection_display(choice.display, default_item)}{choice.id}:\t{choice.display}'
                  for choice in choices]

    print('\n'.join(to_display))
    return choices



def pick(items: list[str], default_item:str='') -> str:
    """ Pick from a list of displayed strings

        Return the selected choice
    """
    # print versions with an associated number
    choices = _display_choice(items, default_item)

    # ask which number to use
    try:
        usr_input = input('Enter the choosen number: ')
    except KeyboardInterrupt:
        print() # print on new line
        exit()

    if not usr_input:
        return default_item

    try:
        # TODO: check no input which means default
        chosen_number = int(usr_input)
    except ValueError:
        print('Incorrect input')
        abort()

    if not 0 <= chosen_number < len(choices):
        print('Incorrect number')
        abort()

    return choices[chosen_number].display



# TODO: move to manager?
def display_versions(versions: list[str], system:str='', local:str=''):
    """List existing Godot applications"""
    to_display = [_verbose_display(version, system, local) for version in versions]

    print('\n'.join(to_display))

