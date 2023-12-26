#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK


from sys import exit, stderr
from colorama import Fore, Style
from colorama import just_fix_windows_console
just_fix_windows_console()

from . import cli
from . import parser
from .manager import AppManager, expand_pattern
from .helpers import abort, current_local_project, platform, architecture
from .paths import DESKTOP_PATH, INSTALL_PATH

try:
    # during build, a version.py module should get generated
    from .version import __version__
except:
    # when using gdvm from the package directly, we get the current version with git
    import subprocess as sp
    try:
        __version__ = sp.run(['git', 'describe', '--tags'], check=False, stdout=sp.PIPE).stdout\
                        .decode('utf-8')\
                        .strip()
        current_branch = sp.run(['git', 'branch', '--show-current'], check=False, stdout=sp.PIPE).stdout\
                           .decode('utf-8')\
                           .strip()
        if current_branch != 'main':
            __version__ = __version__ + ':' + current_branch
    except:
        __version__ = 'version not found'


def main():

    # Parse arguments
    args = parser.parse_args()

    # Display help message when no args are passed.
    if not parser.has_arguments():
        parser.print_help()
        exit()

    if args.subparser_name is None and args.version:
        print(__version__)
        exit()


    app_manager = AppManager()

    def pick_version(default_item='system'):
        # TODO: select multiple versions in version picker
        if default_item == 'system':
            default = app_manager.system_version
        else:
            default = ''

        return app_manager.pick_version(default=default)



    if (args.subparser_name is None and args.list) or args.subparser_name == 'list':
        app_manager.display_versions()
        exit()


    def check_gdvm_release():
        from . import upgrade as up
        latest = up.latest_release()
        if up.is_more_recent_than_current(latest):
            print(f'{Fore.YELLOW}A new version of gdvm is available ({latest}), consider upgrading with: gdvm upgrade{Style.RESET_ALL}')


    if args.subparser_name == 'sync':
        check_gdvm_release()

        from .downloader.godotwebsite import sync
        sync()

        exit()


    if args.subparser_name == 'run':
        if args.version:
            app_manager[args.version].run()
            exit()

        local_project = current_local_project()

        if args.system:
            app_manager.run_system_version()
        elif local_project or args.local:
            if local_project:
                print(f'{Fore.YELLOW}Found project with local version: {local_project}{Style.RESET_ALL}')

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
            version = pick_version()
            app_manager[version].run()


    if args.subparser_name == 'use':
        version = args.version if args.version else pick_version()
        chosen_app = app_manager[version]
        app_manager.install(chosen_app, system=args.system_default) # defaults to local


    if args.subparser_name == 'deactivate':
        try:
            match args.dac_subparser_name:

                case 'system-default':
                    if not app_manager.system_version:
                        print('No default system Godot found')
                        abort()

                    match input(f"""Deactivate system's default Godot {Fore.YELLOW}{INSTALL_PATH}{Style.RESET_ALL}? [y/N]: """):
                        case 'y':
                            import os
                            os.remove(DESKTOP_PATH)
                            os.remove(INSTALL_PATH)
                            print(f'Removed {INSTALL_PATH}')
                        case _:
                            abort()

                case 'local':
                    local_project = current_local_project()
                    if not local_project:
                        print('No local version found')
                        abort()

                    match input(f'Deactivate local version for {Fore.YELLOW}{local_project}{Style.RESET_ALL} ? [y/N]: '):
                        case 'y':
                            import os
                            gdversion_file = os.path.join(local_project,'.godotversion')
                            os.remove(gdversion_file)
                            print(f'Removed {gdversion_file}')
                        case _:
                            abort()

                case _:
                    parser.print_help(args.subparser_name)

        except KeyboardInterrupt:
            print()
            abort()

        exit()


    if args.subparser_name == 'add':
        if isinstance(args.file, list):
            for f in args.file:
                try:
                    app_manager.add(f)
                except KeyboardInterrupt:
                    abort()
                except:
                    print(f'installation cancelled')
        else:
            try:
                app_manager.add(args.file)
            except KeyboardInterrupt:
                abort()
            except:
                print(f'installation cancelled')


    if args.subparser_name == 'remove':
        versions = args.version if args.version else [pick_version(default_item='')]
        versions = expand_pattern(versions)

        chosen_apps = [app_manager[version] for version in versions]

        if args.force:
            for app in chosen_apps:
                app_manager.remove(app)
            exit()

        match input(f'Are you sure you want to remove {", ".join(app.version for app in chosen_apps)}? [y/N]: '):
            case 'y':
                for app in chosen_apps:
                    app_manager.remove(app)
                exit()
            case other:
                abort()


    if args.subparser_name == 'download':
        check_gdvm_release()

        from .downloader import downloader as dl

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

        remote_versions = list(dl.version_numbers())
        if args.versions:
            versions = args.versions
        else:
            versions = cli.pick(remote_versions, remote_versions[0])

        for version in expand_pattern(versions, targets=remote_versions):
            if release == 'latest':
                release = dl.latest_release(version)

            releases = list(dl.release_names(version))
            if (not args.versions) or (release not in releases):
                default_release = 'stable' if 'stable' in releases else releases[-1]
                release = cli.pick(releases, default_release)

            try:
                dl_file = dl.download_app(version,
                                          system=system,
                                          architecture=arch,
                                          mono=args.mono,
                                          release=release)
            except KeyboardInterrupt:
                abort()

            if add_to_manage:
                try:
                    app_manager.add(dl_file)
                except KeyboardInterrupt:
                    abort()
                except:
                    print(f'installation cancelled')
            else:
                print(f"Downloaded {dl_file} but didn't add it to managed apps because it doesn't fit your system")


    if args.subparser_name == 'config':
        # self_contain version can be nested in case of wildcard use
        for version in expand_pattern(args.self_contain):
            app_manager[version].selfcontain = True
        for version in expand_pattern(args.share_container):
            app_manager[version].selfcontain = False


    if args.subparser_name == 'upgrade':
        print('Looking for a new gdvm release...')
        from . import upgrade as up
        latest = up.latest_release()
        if not up.is_more_recent_than_current(latest):
            print('Already up to date')
            exit()

        match input(f'{latest} is available, do you want to upgrade? [y/N]: ').lower():
            case 'y' | 'yes':
                up.upgrade(latest)
                exit()
            case _:
                abort()






if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=stderr)
    exit(rc)
