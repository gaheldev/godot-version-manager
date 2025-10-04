import sys
import argparse
import argcomplete
import os

from .completers import FilteredFilesCompleter, InstalledVersionsCompleter, GodotVersionsCompleter




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

parser_add.add_argument('file', metavar='FILE',
                        nargs='+',
                        help='Godot binary or zip archive')\
          .completer = FilteredFilesCompleter(lambda f: os.path.basename(f).startswith('Godot_'))


# Delete Godot version
parser_del = subparsers.add_parser('remove',
                                   aliases=['rm'],
                                   help='delete Godot version from managed versions')

parser_del.add_argument('-f', '--force',
                        action='store_true',
                        help='remove version without asking for confirmation')

parser_del.add_argument('version', metavar='VERSION',
                        nargs='*',
                        help='version(s) of the installed Godot app to remove')\
          .completer = InstalledVersionsCompleter(argument='version')



# Stop using version as local or system's default
parser_dac = subparsers.add_parser('deactivate',
                                   help="""deactivate local or system's default Godot version""")

dac_subparsers = parser_dac.add_subparsers(dest='dac_subparser_name')

dac_subparsers.add_parser('system-default',
                          help="""deactivate system's default Godot and its desktop shortcut (if any)""")

dac_subparsers.add_parser('local',
                          help='stop using a local Godot version in the current project (if any)')



# Optional listing of available Godot version
parser_list = subparsers.add_parser('list', aliases=['ls'], help=f'list managed Godot versions')


# Display current gdvm version
main_parser.add_argument('-v', '--version', action='store_true',
                         help=f'display gdvm version')


# Start Godot
parser_run = subparsers.add_parser('run',
                                   help='launch godot (defaults to --local if a project version is defined)')

run_group = parser_run.add_mutually_exclusive_group()
run_group.add_argument('version', metavar='VERSION',
                       nargs='?',
                       help='Godot version to run (e.g. 3.4, 4.1.1, ...)')\
         .completer = InstalledVersionsCompleter()

run_group.add_argument('--system', action='store_true',
                       help='run system Godot version')

run_group.add_argument('--local', action='store_true',
                       help='launch local Godot version from current working directory .godotversion file')


# Get list of available versions
parser_sync = subparsers.add_parser('sync', help='get latest list of Godot builds')


# Configure stuff
parser_config = subparsers.add_parser('config', help='')

contain_group = parser_config.add_mutually_exclusive_group()
contain_group.add_argument('--self-contain',
                           default='', metavar=('VERSION'),
                           nargs='+',
                           help='self contain chosen Godot versions')\
             .completer = InstalledVersionsCompleter(argument='self_contain',
                                                     filter=lambda app: not app.selfcontain)

contain_group.add_argument('--no-self-contain',
                           default='', metavar=('VERSION'),
                           nargs='+',
                           help='use shared config for chosen Godot versions')\
             .completer = InstalledVersionsCompleter(argument='no_self_contain',
                                                     filter=lambda app: app.selfcontain)


# Download godot version
parser_dl = subparsers.add_parser('download', aliases=['dl'], help='download Godot versions (add to managed if compatible with system)')

parser_dl.add_argument('versions', metavar='VERSION',
                       nargs='*',
                       help='Godot versions to download (e.g. 3.4, 4.1.x, 4.x.1-rcx, ...)')\
         .completer = GodotVersionsCompleter()

parser_dl.add_argument('--system',
                       default='', choices=['linux', 'windows', 'osx'],
                       metavar=('SYSTEM'),
                       help='system build ( linux | windows | osx)')

parser_dl.add_argument('--arch', metavar=('ARCH'),
                       default='', choices=['32', '64'],
                       help='system architecture ( 32 | 64 )')

parser_dl.add_argument('--mono', action='store_true', help='mono build')


# Upgrade gdvm
parser_up = subparsers.add_parser('upgrade', help='upgrade gdvm to latest release')



def parse_args(*args,**kwargs):
    argcomplete.autocomplete(main_parser, always_complete_options='long')
    return main_parser.parse_args(*args,**kwargs)


def print_help(subparser_name: str=''):
    if not subparser_name:
        main_parser.print_help()
        return

    main_parser.parse_args([subparser_name, '--help'])



def has_arguments() -> bool:
    return len(sys.argv)!=1
