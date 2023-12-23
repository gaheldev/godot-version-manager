from collections import namedtuple
from colorama import Fore, Style
from sys import exit

from .helpers import abort




def _selection_display(item: str, default_item:str='') -> str:
    if not default_item:
        return ''

    if default_item == item:
        return '-> '
    else:
        return '   '


def _used_display(item: str, system:str='', local:str='') -> str:
    suffix = ''
    if item == system:
        suffix += f'{Fore.RED} System'
    if item == local:
        suffix += f'{Fore.YELLOW} Local'
    if suffix:
        suffix += f'{Style.RESET_ALL}'
    return suffix



def _verbose_display(item: str, system:str='', local:str='') -> str:
    default_item = ''
    if local:
        default_item = local
    elif system:
        default_item = system

    suffix = _used_display(item, system, local)

    return f'{_selection_display(item, default_item)}{item}{suffix}'



Choice = namedtuple('Choice', 'id display')

def _display_choice(displays: list[str], default_item:str='',
                    system:str='', local:str='') -> list[Choice]:
    """Display a list of choices with an associated number

       Return a Choice(id,display) named tuple
    """
    choices = [Choice(id,display)
               for id, display in enumerate(displays)]

    to_display = [f'{_selection_display(choice.display, default_item)}{choice.id}:\t{choice.display}{_used_display(choice.display, system, local)}'
                  for choice in choices]

    print('\n'.join(to_display))
    return choices



def pick(items: list[str], default_item:str='',
         system:str='', local:str='') -> str:
    """ Pick from a list of displayed strings

        Return the selected choice
    """
    if len(items) == 0:
        print('No installed versions found, please use gdvm download or gdvm add')
        abort()

    # print versions with an associated number
    choices = _display_choice(items, default_item, system, local)

    def default_str():
        if not default_item:
            return ''
        for i, item in enumerate(items):
            if item == default_item:
                return f' (default={i})'

    # ask which number to use
    try:
        usr_input = input(f'Enter the choosen number{default_str()}: ')
    except KeyboardInterrupt:
        print() # print on new line
        exit()

    if not usr_input:
        if not default_item:
            print('No item selected')
            exit()
        return default_item

    try:
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

