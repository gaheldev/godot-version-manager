from collections import namedtuple

from helpers import abort




def _selection_display(item: str, default_item: str) -> str:
    if default_item == item:
        return '-> '
    else:
        return '   '



Choice = namedtuple('Choice', 'id display')

def _display_choice(default_item, displays: list[str]) -> list[Choice]:
    """Display a list of choices with an associated number

       Return a Choice(id,display) named tuple
    """
    choices = [Choice(id,display)
               for id, display in enumerate(displays)]

    to_display = [f'{_selection_display(choice.display, default_item)}{choice.id}:\t{choice.display}'
                  for choice in choices]

    print('\n'.join(to_display))
    return choices



def pick(default_item, items: list[str]) -> str:
    """ Pick from a list of displayed strings

        Return the selected choice
    """
    # print versions with an associated number
    choices = _display_choice(default_item,items)

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



# TODO: move to manager
def display_versions(current_version: str, versions: list[str]):
    """List existing Godot applications"""
    to_display = [f'{_selection_display(version, current_version)}{version}'
                  for version in versions]

    print('\n'.join(to_display))

