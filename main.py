#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import cli
from manager import AppManager, GodotApp, SAVE_DIR
from helpers import abort, gvmfile_in_cwd
from sys import exit
from downloader import download_app
import os




# Parse arguments
args = cli.parse_args()

# Display help message when no args are passed.
if not cli.has_arguments():
    cli.print_help()
    exit()


app_manager = AppManager()


if args.list or args.subparser_name == 'list':
    cli.display_versions(app_manager)
    exit()


if args.subparser_name == 'run':
    if args.system:
        app_manager.run_system_version()
    elif gvmfile_in_cwd() or args.local:
        app_manager.run_project_version()
    else:
        chosen_app = cli.pick_version(app_manager)
        chosen_app.run()


if args.subparser_name == 'use':
    chosen_app = cli.pick_version(app_manager)
    app_manager.install(chosen_app, project=args.local)


if args.subparser_name == 'add':
    app_manager.add(args.file)


if args.subparser_name == 'remove':
    if args.APP:
        chosen_app = GodotApp(os.path.join(SAVE_DIR, args.APP))
    else:
        chosen_app = cli.pick_version(app_manager)

    match input(f'Are you sure you want to remove {chosen_app.version}? [y/N]: '):
        case 'y':
            app_manager.remove(chosen_app)
        case other:
            abort()


if args.subparser_name == 'install':
    if args.from_file:
        app_manager.install(args.from_file)
    elif args.from_repo:
        dl = download_app(args.from_repo)
        app_manager.install(dl)
    else:
        cli.print_help()


if args.subparser_name == 'download':
    dl = download_app(args.version,
                      system=args.system,
                      architecture=args.arch,
                      prerelease=args.pre_release)
    app_manager.add(dl)
