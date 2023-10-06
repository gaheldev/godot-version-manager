#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from sys import exit

import cli
import parser
import manager
from manager import AppManager
from helpers import abort, gvmfile_in_cwd, platform, architecture
import downloader as dl


def pick_version():
    # TODO: select multiple versions in version picker
    return cli.pick(app_manager.versions, manager.get_current_version())



# Parse arguments
args = parser.parse_args()

# Display help message when no args are passed.
if not parser.has_arguments():
    parser.print_help()
    exit()


app_manager = AppManager()


if args.list or args.subparser_name == 'list':
    cli.display_versions(app_manager.versions, manager.get_current_version())
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
    arch = architecture()
    release = args.release
    add_to_manage = True

    if args.system:
        if system != args.system:
            add_to_manage = False
        system = args.system

    if args.arch:
        if arch != args.arch:
            add_to_manage = False
        arch = args.arch

    if args.version:
        version = args.version
    else:
        versions = list(dl.get_version_numbers())
        version = cli.pick(versions, versions[-1])

    releases = list(dl.get_release_names(version))
    if (not args.version) or (release not in releases):
        default_release = 'stable' if 'stable' in releases else releases[-1]
        release = cli.pick(releases, default_release)

    dl_file = dl.download_app(version,
                              system=system,
                              architecture=arch,
                              mono=args.mono,
                              release=release)

    if add_to_manage:
        app_manager.add(dl_file)
    else:
        print(f"Downloaded {dl_file} but didn't add it to managed apps because it doesn't fit your system")
