from collections import namedtuple

import manager
from helpers import abort




def _selection_display(version: str) -> str:
    if version == manager.get_current_version():
        return '-> '
    else:
        return '   '



Choice = namedtuple('Choice', 'id version')

def _display_version_choice(app_manager: manager.AppManager) -> list[Choice]:
    """Display a list of managed Godot versions with an associated number

       Return a Choice(id,version) named tuple
    """
    choices = [Choice(i, version) for i, version in enumerate(app_manager.versions)]

    to_display = [f'{_selection_display(choice.version)}{choice.id}:\t{choice.version}'
                  for choice in choices]

    print('\n'.join(to_display))
    return choices



def pick_version(app_manager: manager.AppManager) -> manager.GodotApp:
    """Pick a Godot version from the list of managed versions

    Return the path to the corresponding Godot binary and the chosen version
    """
    # print versions with an associated number
    choices = _display_version_choice(app_manager)

    # ask which number to use
    try:
        usr_input = input('Enter the choosen number: ')
    except KeyboardInterrupt:
        print() # print on new line
        exit()

    try:
        chosen_number = int(usr_input)
    except ValueError:
        print('Incorrect input')
        abort()

    if not 0 <= chosen_number < len(choices):
        print('Incorrect number')
        abort()

    return app_manager.get_app_from_version(choices[chosen_number].version)



def display_versions(app_manager: manager.AppManager):
    """List existing Godot applications"""
    to_display = [f'{_selection_display(version)}{version}'
                  for version in app_manager.versions]

    print('\n'.join(to_display))

