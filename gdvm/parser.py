import sys
import argparse
import argcomplete
import os

from .completers import FilteredFilesCompleter, GodotReleasesCompleter, GodotVersionNumbersCompleter, InstalledVersionsCompleter




# Instantiate the parser
main_parser = argparse.ArgumentParser(description='Manage Godot versions')
subparsers = main_parser.add_subparsers(dest='subparser_name')




# Change Godot version
parser_use = subparsers.add_parser('use', help='pick the Godot version to use system wise or locally')

parser_use.add_argument('version', metavar='VERSION',
                        nargs='?',
                        help='version of Godot to use from managed versions')\
          .completer = InstalledVersionsCompleter()

parser_use.add_argument('--system-default', action='store_true',
                        help='pick the Godot version to use system wise')


# Add archive file without installing
parser_add = subparsers.add_parser('add',
                                   help='add Godot binary or zip archive to managed versions')

parser_add.add_argument('file', metavar='FILE', help='Godot binary or zip archive')\
          .completer = FilteredFilesCompleter(lambda f: os.path.basename(f).startswith('Godot_'))


# Delete Godot version
parser_del = subparsers.add_parser('remove',
                                   help='delete Godot version from managed versions')

parser_del.add_argument('-f', '--force',
                        action='store_true',
                        help='remove version without asking for confirmation')

parser_del.add_argument('version', metavar='VERSION',
                        nargs='*',
                        help='version(s) of the installed Godot app to remove')\
          .completer = InstalledVersionsCompleter()



# Stop using version as local or system's default
parser_dac = subparsers.add_parser('deactivate',
                                   help="""deactivate local or system's default Godot version""")

dac_subparsers = parser_dac.add_subparsers(dest='dac_subparser_name')

dac_subparsers.add_parser('system-default',
                          help="""deactivate system's default Godot and its desktop shortcut (if any)""")

dac_subparsers.add_parser('local',
                          help='stop using a local Godot version in the current project (if any)')



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
          .completer = InstalledVersionsCompleter()

parser_run.add_argument('--system', action='store_true',
                        help='run system Godot version')

parser_run.add_argument('--local', action='store_true',
                        help='launch local Godot version from current working directory .godotversion file')


# Download godot version
parser_sync = subparsers.add_parser('sync', help='get latest list of Godot builds')


# Download godot version
parser_dl = subparsers.add_parser('download', help='download a Godot version (add to managed if compatible with system)')

parser_dl.add_argument('version', metavar='VERSION',
                       nargs='?',
                       help='Godot version to download (e.g. 3.4, 4.1.1, ...)')\
         .completer = GodotVersionNumbersCompleter()

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
         .completer = GodotReleasesCompleter()


# Upgrade gdvm
parser_up = subparsers.add_parser('upgrade', help='upgrade gdvm to latest release')



def parse_args(*args,**kwargs):
    argcomplete.autocomplete(main_parser)
    return main_parser.parse_args(*args,**kwargs)


def print_help():
    main_parser.print_help()


def has_arguments() -> bool:
    return len(sys.argv)!=1
