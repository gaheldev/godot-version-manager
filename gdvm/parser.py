import sys
import argparse
import argcomplete
import os

from .downloader import downloader
from . import manager
from .completers import FilteredFilesCompleter, c_releases




# Instantiate the parser
main_parser = argparse.ArgumentParser(description='Manage Godot versions')
subparsers = main_parser.add_subparsers(dest='subparser_name')




# Change Godot version
parser_use = subparsers.add_parser('use', help='pick the Godot version to use system wise or locally')

parser_use.add_argument('version', metavar='VERSION',
                        nargs='?',
                        help='version of Godot to use from managed versions')\
          .completer = argcomplete.ChoicesCompleter(manager.get_installed_versions())

parser_use.add_argument('--system-default', action='store_true',
                        help='pick the Godot version to use system wise')

parser_use.add_argument('--local', action='store_true',
                        help='pick the Godot version to use in the current folder')


# Add archive file without installing
parser_add = subparsers.add_parser('add',
                                   help='add Godot binary or zip archive to managed versions')

parser_add.add_argument('file', metavar='FILE', help='Godot binary or zip archive')\
          .completer = FilteredFilesCompleter(lambda f: os.path.basename(f).startswith('Godot_'))


# Delete Godot version
parser_del = subparsers.add_parser('remove',
                                   help='delete Godot version from managed versions (remain installed system wise if currently in use)')

parser_del.add_argument('-f', '--force',
                        action='store_true',
                        help='remove version without asking for confirmation')

parser_del.add_argument('version', metavar='VERSION',
                        nargs='*',
                        help='version(s) of the installed Godot app to remove')\
          .completer = argcomplete.ChoicesCompleter(manager.get_installed_versions())



# Optional listing of available Godot version
parser_list = subparsers.add_parser('list', help=f'list managed Godot versions')

main_parser.add_argument('-l', '--list', action='store_true',
                         help=f'list managed Godot versions')

# Display current gdvm version
main_parser.add_argument('-v', '--version', action='store_true',
                         help=f'display gdvm version')


# Start Godot
parser_run = subparsers.add_parser('run',
                                   help='launch godot (defaults to --local if .godotversion file exists in current working directory)')

parser_run.add_argument('version', metavar='VERSION',
                        nargs='?',
                        help='Godot version to run (e.g. 3.4, 4.1.1, ...)')\
          .completer = argcomplete.ChoicesCompleter(manager.get_installed_versions())

parser_run.add_argument('--system', action='store_true',
                        help='run system Godot version')

parser_run.add_argument('--local', action='store_true',
                        help='launch local Godot version from current working directory .godotversion file')


# Download godot version
parser_dl = subparsers.add_parser('download', help='download a Godot version (add to managed if compatible with system)')

parser_dl.add_argument('version', metavar='VERSION',
                       nargs='?',
                       help='Godot version to download (e.g. 3.4, 4.1.1, ...)')\
         .completer = argcomplete.ChoicesCompleter(downloader.get_version_numbers())

parser_dl.add_argument('--system',
                       default='', choices=['linux', 'windows', 'osx'],
                       metavar=('SYSTEM'),
                       help='system build ( linux | windows | osx)')

parser_dl.add_argument('--arch', metavar=('ARCH'),
                       default='', choices=['32', '64'],
                       help='system architecture ( 32 | 64 )')

parser_dl.add_argument('--mono', action='store_true', help='mono build')

parser_dl.add_argument('--release',
                       default='stable', metavar=('RELEASE'),
                       help='stable (default), alpha, beta, rc or dev release')\
         .completer = c_releases


# Upgrade gdvm
parser_up = subparsers.add_parser('upgrade', help='upgrade gdvm to latest release')



def parse_args(*args,**kwargs):
    argcomplete.autocomplete(main_parser)
    return main_parser.parse_args(*args,**kwargs)


def print_help():
    main_parser.print_help()


def has_arguments() -> bool:
    return len(sys.argv)!=1
