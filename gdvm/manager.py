import os

from os.path import basename
from typing import Generator
from colorama import Fore, Style
import shutil
from functools import cached_property

from .data import GodotApp, get_mono_app, app_path_from, version, current_system_version, short_version
from .helpers import extract_archive, abort, parse_version, platform, architecture, current_local_project, wildcard_fullmatch
from .paths import CACHE_DIR, APP_DIR, TMP_DIR
from .downloader.downloader import download_app
from . import cli




os.makedirs(CACHE_DIR,exist_ok=True)
os.makedirs(APP_DIR,exist_ok=True)



def installed_apps() -> Generator[GodotApp, None, None]:
    with os.scandir(APP_DIR) as it:
        for file in it:
            if not file.is_dir:
                continue
            app_path = app_path_from(file.path)
            if app_path:
                yield GodotApp(app_path)



def installed_versions() -> Generator[str, None, None]:
    for app in installed_apps():
        yield app.short_version



def expand_pattern(versions: str | list[str] | Generator[str, None, None],
                   targets:list=list(installed_versions()),
                   ) -> Generator[str, None, None]:
    if not versions:
        return # empty generator

    if isinstance(versions, str):
        versions = [versions]

    cache = set()
    for version in versions:
        if version in cache:
            continue

        if not 'x' in version:
            yield version
            cache.add(version)
            continue

        for target in targets:
            if wildcard_fullmatch(version, target):
                if not target in cache:
                    yield target
                    cache.add(version) # pattern
                    cache.add(target) # match



def is_valid_app(app_path: str) -> bool:
    try:
        version(app_path)
    except:
        Warning(f'Cannot get Godot version from {basename(app_path)}')
        return False
    return True




class AppManager:
    def __init__(self):
        if self._has_old_saved_apps():
            print('Migrating managed apps to new format...')
            self.apps = []
            self._migrate_old_apps()

        self.apps: list[GodotApp] = [GodotApp(path) 
                                     for path in self.list_apps_paths()
                                     if is_valid_app(path)]
        self.apps.sort(reverse=True)


    def list_apps_paths(self) -> Generator[str, None, None]:
        """ return paths to Godot executables in APP_DIR """
        for f in os.scandir(APP_DIR):
            if f.is_dir():
                yield os.path.join(APP_DIR, f, app_path_from(f))


    def _has_old_saved_apps(self) -> bool:
        for f in os.scandir(APP_DIR):
            if 'Godot_v' in f.name:
                return True
        return False


    def _migrate_old_apps(self):
        for f in os.scandir(APP_DIR):
            if 'Godot_v' in f.name:
                self.add(f.path)


    def add(self, godot_path: str) -> GodotApp:
        # TODO: 
        #       - support multiple kind of arguments (version, version number ...)
        #       - check app is already managed
        return self._add_archive(godot_path)


    def _add_archive(self, godot_path: str) -> GodotApp:
        """Add Godot app to the managed versions

        If the godot_path is a zip archive downloaded from Godot website,
        it is extracted first

        For mono builds, the godot_path should be either an archive or the extracted folder
        """
        # extract the zip archive if necessary
        flag_archive = False
        if godot_path.endswith('.zip'):
            godot_path = extract_archive(godot_path, TMP_DIR)
            flag_archive = True

        if os.path.isfile(godot_path):
            godot_exe = godot_path
        elif os.path.isdir(godot_path):
            godot_exe = get_mono_app(godot_path)
        else:
            print(f'{Fore.RED}{godot_path} is not valid{Style.RESET_ALL}')
            abort()

        # make sure the file is executable
        os.chmod(godot_exe, os.stat(godot_exe).st_mode | 0o111)

        if not is_valid_app(godot_exe):
            if flag_archive:
                os.remove(godot_path)
            print(f'{Fore.RED}{godot_path} is not valid{Style.RESET_ALL}')
            abort()

        tmp_app = GodotApp(godot_exe)

        if tmp_app.short_version in self.versions:
            match input(f'{Fore.RED}{tmp_app.short_version} is already installed, reinstall? (all config of this version will be lost) [y/N]: {Style.RESET_ALL}').lower():
                case 'y' | 'yes':
                    self[tmp_app.short_version].remove()
                case _:
                    raise Exception('Installation cancelled')

        print(f'{Fore.YELLOW}Installing {os.path.basename(godot_exe)}...{Style.RESET_ALL}')

        # add to the list of managed versions
        output_exe = os.path.join(APP_DIR, tmp_app.short_version, basename(godot_exe))
        output_dir = os.path.dirname(output_exe)
        print(f'Saving a copy to {output_dir}')

        if os.path.isfile(godot_path):
            os.makedirs(output_dir, exist_ok=True)
            if flag_archive:
                shutil.move(godot_exe, output_exe) # gets rid of the extracted archive in TMP
            else:
                shutil.copy2(godot_exe, output_exe) # copy with permissions, keep the original
        else:
            if flag_archive:
                shutil.move(godot_exe, output_exe)
            else:
                shutil.copy2(godot_path, output_dir)

        new_app = GodotApp(output_exe)
        self.apps.append(new_app)
        return new_app


    @property
    def paths(self) -> list[str]:
        return [app.path for app in self.apps]


    @property
    def versions(self) -> list[str]:
        return [app.short_version for app in self.apps]


    @cached_property
    def project_version(self) -> str:
        v = self.project_long_version
        return short_version(v) if v else ''


    @cached_property
    def current_project(self) -> str | None:
        return current_local_project()


    @cached_property
    def project_long_version(self) -> str:
        local_version = ''
        if self.current_project:
            gdversion_file = os.path.join(self.current_project, '.godotversion')
            with open(gdversion_file) as f:
                local_version = f.read().strip()
        return local_version


    @cached_property
    def system_version(self) -> str:
        return current_system_version()


    def __getitem__(self, version: str) -> GodotApp:
        """ accepts either complete or short version """
        for app in self.apps:
            if (app.version == version) or (app.short_version == version):
                return app
        raise LookupError(f'{version} is not installed')


    def install(self, app: str|GodotApp, system=False):
        """Install as system Godot version (system=True) or define as Godot
           version for use in the current directory (system=False)

           app: path or GodotApp 
        """
        if type(app) is str:
            self.add(app).install(system)
        elif type(app) is GodotApp:
            app.install(system)


    def add_version(self, version: str):
        version_number, release, mono = parse_version(version)
        archive = download_app(version_number,
                               release=release,
                               system=platform(),
                               mono=mono,
                               architecture=architecture())
        self.add(archive)


    def remove(self, app: GodotApp):
        app.remove()
        print(f'Removed {app.version}')


    def run_system_version(self):
        version = self.system_version
        if version == '':
            print('System version is not defined')
            abort()
        system_app = self[version]
        system_app.run()


    def run_project_version(self):
        if self.project_version:
            project_app = self[self.project_version]
            project_app.run()


    def _display_suffix(self, app: GodotApp) -> str:
        suffix = Style.RESET_ALL
        if app.short_version == self.project_version:
            suffix += f'{Fore.YELLOW} Local'
        if app.short_version == self.system_version:
            suffix += f'{Fore.RED} System'
        if app.selfcontain:
            suffix += f'{Fore.BLUE} sc'
        if suffix:
            suffix += f'{Style.RESET_ALL}'
        return suffix


    def display_versions(self, no_default=False, hilight=True, numbered=False) -> None:
        """List existing Godot applications"""
        padding = True
        if not self.system_version and not self.project_version:
            padding = False

        default_version = self.project_version or self.system_version

        for i, app in enumerate(self.apps):
            selected = app.short_version == default_version

            if no_default:
                padding = False
                selected = False

            repr = cli.item_repr(app.short_version,
                                 number=(i if numbered else None),
                                 padding=padding,
                                 selected=selected)

            style = ''
            if selected and hilight:
                if default_version == self.project_version:
                    style = Fore.YELLOW
                elif default_version == self.system_version:
                    style = Fore.RED

            print(f'{style}{repr}{self._display_suffix(app)}')


    def pick_version(self, default:str = '') -> str|None:
        """Pick a managed version from the command line"""
        if len(self.apps) == 0:
            print('No installed versions found, please use gdvm download or gdvm add')
            abort()

        self.display_versions(no_default=(default == ''),
                              hilight=False,
                              numbered=True)

        choices = [cli.Choice(i, app.short_version)
                   for i, app in enumerate(self.apps)]

        if not default:
            return cli.pick_choice(choices).display or ''

        for c in choices:
            if c.display == default:
                return cli.pick_choice(choices, default=c).display
