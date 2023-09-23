#!/usr/bin/env python3

import cli
from manager import AppManager
from helpers import abort, gvmfile_in_cwd




# Parse arguments
args = cli.parse_args()

# Display help message when no args are passed.
if not cli.has_arguments():
    cli.print_help()
    exit()


app_manager = AppManager()


if args.subparser_name == 'list':
    cli.display_versions(app_manager)


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
    chosen_app = cli.pick_version(app_manager)
    match input(f'Are you sure you want to remove {chosen_app.version}? [y/N]: '):
        case 'y':
            app_manager.remove(chosen_app)
        case other:
            abort()


if args.subparser_name == 'install':
    if args.file:
        app_manager.install(args.file)
    else:
        cli.print_help()


if args.subparser_name == 'download':
    import downloader as d
    d.download_app(args.version, args.system, args.arch)
