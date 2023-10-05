#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from sys import exit

import cli
import parser
import manager
from manager import AppManager
from helpers import abort, gvmfile_in_cwd, platform
from downloader import download_app


def pick_version():
    # TODO: select multiple versions in version picker
    return cli.pick(manager.get_current_version(), app_manager.versions)



# Parse arguments
args = parser.parse_args()

# Display help message when no args are passed.
if not parser.has_arguments():
    parser.print_help()
    exit()


app_manager = AppManager()


if args.list or args.subparser_name == 'list':
    cli.display_versions(manager.get_current_version(), app_manager.versions)
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
            if project_version:
                app_manager.add_version(project_version)
                app_manager.run_project_version()
            else:
                raise Exception(f'Project version {project_version} unrecognized')

    else:
        # TODO
        version = pick_version()
        app_manager.get_app_from_version(version).run()


if args.subparser_name == 'use':
    version = args.version if args.version else pick_version()
    chosen_app = app_manager.get_app_from_version(version)
    app_manager.install(chosen_app, project=args.local)


if args.subparser_name == 'add':
    app_manager.add(args.file)


if args.subparser_name == 'remove':
    versions = args.version if args.version else [pick_version()]

    chosen_apps = [app_manager.get_app_from_version(version) for version in versions]

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
                      mono=args.mono,
                      prerelease=args.pre_release)

    if add_to_manage:
        app_manager.add(dl)
