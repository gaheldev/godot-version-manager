import os

from os.path import basename
from typing import Generator

from .data import GodotApp, get_mono_app, app_path_from, version, current_system_version
from .helpers import extract_archive, abort, parse_version, platform, architecture, current_local_project
from .paths import CACHE_DIR, APP_DIR, TMP_DIR
from .downloader.downloader import download_app




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
        if godot_path.endswith('.zip'):
            godot_path = extract_archive(godot_path, TMP_DIR)

        if os.path.isfile(godot_path):
            godot_exe = godot_path
        elif os.path.isdir(godot_path):
            godot_exe = get_mono_app(godot_path)
        else:
            print(f'{godot_path} is not valid')
            abort()

        # make sure the file is executable
        os.chmod(godot_exe, os.stat(godot_exe).st_mode | 0o111)

        if not is_valid_app(godot_exe):
            os.remove(godot_path)
            print(f'{godot_path} is not valid')
            abort()

        # add to the list of managed versions
        tmp_app = GodotApp(godot_exe)
        if os.path.isfile(godot_path):
            output_exe = os.path.join(APP_DIR, tmp_app.short_version, basename(godot_exe))
            output_dir = os.path.dirname(output_exe)
            os.makedirs(output_dir, exist_ok=True)
            print(f'Saving a copy to {output_dir}')
            os.rename(godot_exe, output_exe)
            new_app = GodotApp(output_exe)
        else:
            output_path = os.path.join(APP_DIR, tmp_app.short_version)
            os.makedirs(output_path, exist_ok=True)
            print(f'Saving a copy to {output_path}')
            os.rename(godot_path, output_path)
            new_app = GodotApp(output_path)

        self.apps.append(new_app)
        return new_app


    @property
    def paths(self) -> list[str]:
        return [app.path for app in self.apps]


    @property
    def versions(self) -> list[str]:
        return [app.short_version for app in self.apps]


    @property
    def project_version(self) -> str:
        try:
            return self[self.project_long_version].short_version
        except:
            return ''


    @property
    def current_project(self) -> str | None:
        return current_local_project()


    @property
    def project_long_version(self) -> str:
        local_version = ''
        if self.current_project:
            gdversion_file = os.path.join(self.current_project, '.godotversion')
            with open(gdversion_file) as f:
                local_version = f.read()
        return local_version


    @property
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


