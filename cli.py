import sys
import argparse
import argcomplete
from collections import namedtuple

import manager
import downloader
from helpers import abort




# Instantiate the parser
main_parser = argparse.ArgumentParser(description='Install Godot system wise and manage versions')
subparsers = main_parser.add_subparsers(dest='subparser_name')




# Install archive file
parser_install = subparsers.add_parser('install', help='install system wise from binary or zip archive')

parser_install.add_argument('--from-file', metavar='FILE', help='Godot binary or zip archive')

parser_install.add_argument('--from-repo', metavar='VERSION', help='install from online Godot repository')\
              .completer = argcomplete.ChoicesCompleter(downloader.get_version_numbers())


# Change Godot version
parser_use = subparsers.add_parser('use', help='pick the Godot version to use system wise or locally')

parser_use.add_argument('--system', action='store_true',
                        help='pick the Godot version to use system wise')

parser_use.add_argument('--local', action='store_true',
                        help='pick the Godot version to use in the current folder')


# Add archive file without installing
parser_add = subparsers.add_parser('add', help='add managed version from binary or zip archive without installing')
parser_add.add_argument('FILE', help='Godot binary or zip archive')


# Delete Godot version
parser_del = subparsers.add_parser('remove', help='delete Godot version (remain installed system wise if currently in use)')

parser_del.add_argument('APP', help='name of the installed Godot app to remove')\
          .completer = argcomplete.ChoicesCompleter(manager.get_installed_apps())



# Optional listing of available Godot version
parser_list = subparsers.add_parser('list', help=f'list available Godot versions')

main_parser.add_argument('-l', '--list', action='store_true',
                         help=f'list available Godot versions')


# Start Godot
parser_run = subparsers.add_parser('run', help='launch godot (defaults to --local if .gvm file exists in current working directory)')

parser_run.add_argument('--system', action='store_true',
                        help='run system Godot version')

parser_run.add_argument('--local', action='store_true',
                        help='launch local Godot version from current working directory .gvm file')


# Download godot version
parser_dl = subparsers.add_parser('download', help='download a Godot version to /tmp')

parser_dl.add_argument('version', metavar='VERSION',
                       help='Godot version to download (e.g. 3.4, 4.1.1, ...)')\
         .completer = argcomplete.ChoicesCompleter(downloader.get_version_numbers())

parser_dl.add_argument('--system',
                       default='linux', choices=['linux', 'windows'],
                       metavar=('SYSTEM'),
                       help='system build ( linux | windows )')

parser_dl.add_argument('--arch',
                       default='64', metavar=('ARCH'),
                       help='system architecture ( 32 | 64 )')

# parser_dl.add_argument('--mono', action='store_true', help='mono build')

release = parser_dl.add_mutually_exclusive_group(required=False)
release.add_argument('--stable', action='store_true', help='stable release')
release.add_argument('--rc', metavar='NUMBER', help='release candidate')
release.add_argument('--alpha', metavar='NUMBER', help='alpha release')
release.add_argument('--beta', metavar='NUMBER', help='beta release')



def parse_args():
    argcomplete.autocomplete(main_parser)
    return main_parser.parse_args()

def print_help():
    main_parser.print_help()

def has_arguments() -> bool:
    return len(sys.argv)!=1




def selection_display(version: str) -> str:
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

    to_display = [f'{selection_display(choice.version)}{choice.id}:\t{choice.version}'
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
    to_display = [f'{selection_display(version)}{version}'
                  for version in app_manager.versions]

    print('\n'.join(to_display))

