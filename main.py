#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from sys import exit

import cli
import parser
from manager import AppManager
from helpers import abort, gvmfile_in_cwd, platform
from downloader import download_app



# Parse arguments
args = parser.parse_args()

# Display help message when no args are passed.
if not parser.has_arguments():
    parser.print_help()
    exit()


app_manager = AppManager()


if args.list or args.subparser_name == 'list':
    cli.display_versions(app_manager)
    exit()


if args.subparser_name == 'run':
    if args.version:
        app_manager.get_app_from_version(args.version).run()
        exit()

    if args.system:
        app_manager.run_system_version()
    elif gvmfile_in_cwd() or args.local:
        try:
            app_manager.run_project_version()
        except LookupError:
            project_version = app_manager.project_version
            if project_version is not None:
                app_manager.add_version(app_manager.project_version)
                app_manager.run_project_version()
            else:
                raise Exception('Project version {project_version} unrecognized')

    else:
        chosen_app = cli.pick_version(app_manager)
        chosen_app.run()


if args.subparser_name == 'use':
    if not args.version:
        chosen_app = cli.pick_version(app_manager)
    else:
        chosen_app = app_manager.get_app_from_version(args.version)
    app_manager.install(chosen_app, project=args.local)


if args.subparser_name == 'add':
    app_manager.add(args.file)


if args.subparser_name == 'remove':
    if not args.version:
        chosen_apps = [cli.pick_version(app_manager)] # TODO: select multiple versions in version picker
    else:
        chosen_apps = [app_manager.get_app_from_version(version) for version in args.version]

    if args.force:
        for app in chosen_apps:
            app_manager.remove(app)
        exit()

    match input(f'Are you sure you want to remove {", ".join(app.version for app in chosen_apps)}? [y/N]: '):
        case 'y':
            for app in chosen_apps:
                app_manager.remove(app)
        case other:
            abort()


if args.subparser_name == 'download':
    system = platform()
    add_to_manage = True

    if args.system:
        if system != args.system:
            add_to_manage = False
        system = args.system

    dl = download_app(args.version,
                      system=system,
                      architecture=args.arch,
                      prerelease=args.pre_release)

    if add_to_manage:
        app_manager.add(dl)
