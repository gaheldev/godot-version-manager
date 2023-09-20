import sys
import argparse

import manager
from helpers import abort




# Instantiate the parser
parser = argparse.ArgumentParser(description='Install Godot system wise and manage versions')

# Make arguments mutually exclusive
exclusive_group = parser.add_mutually_exclusive_group()

# Install archive file
exclusive_group.add_argument('-i', '--install', metavar=('ARCHIVE'),
                    help='install Godot system wise from binary or zip archive')

# Change Godot version
exclusive_group.add_argument('-u', '--use', action='store_true',
                    help='pick the Godot version to use system wise')

# Set up local Godot version
exclusive_group.add_argument('-U', '--use-local', action='store_true',
                    help='pick the Godot version to use in the current folder')

# Add archive file without installing
exclusive_group.add_argument('-a', '--add', metavar=('ARCHIVE'),
                    help='add managed version from binary or zip archive without installing')

# Delete Godot version
exclusive_group.add_argument('-d', '--delete', action='store_true',
                             help='delete Godot version (remain installed system wise if currently in use)')

# Optional listing of available Godot version
exclusive_group.add_argument('-l', '--list', action='store_true',
                    help=f'list available Godot versions')

# Launch Godot from a list of available versions
exclusive_group.add_argument('-s', '--start', action='store_true',
                    help='launch Godot from the list of available versions')

# Launch local Godot version from current working directory .gvm file
exclusive_group.add_argument('-S', '--start-local', action='store_true',
                    help='launch local Godot version')


def parse_args():
    return parser.parse_args()

def print_help():
    parser.print_help()

def has_arguments() -> bool:
    return len(sys.argv)!=1




def selection_display(version: str) -> str:
    if version == manager.get_current_version():
        return '-> '
    else:
        return '   '



def display_version_choice() -> list[manager.Choice]:
    """Display a list of managed Godot versions with an associated number

    Return a Choice(id,version,app_path) named tuple
    """
    choices = [manager.Choice(i, manager.get_version(app), app)
               for i, app in enumerate(manager.managed_apps())]

    to_display = [f'{selection_display(choice.version)}{choice.id}:\t{choice.version}'
                  for choice in choices]

    print('\n'.join(to_display))
    return choices



def pick_version() -> tuple:
    """Pick a Godot version from the list of managed versions

    Return the path to the corresponding Godot binary and the chosen version
    """
    # print versions with an associated number
    choices = display_version_choice()

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

    # return the chosen Godot version and its corresponding app path
    chosen_app = choices[chosen_number].path
    chosen_version = choices[chosen_number].version
    return chosen_app, chosen_version



def display_versions():
    """List existing Godot applications"""
    to_display = [f'{selection_display(version)}{version}'
                  for version in manager.versions()]

    print('\n'.join(to_display))

