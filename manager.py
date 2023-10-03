import os
import shutil
import subprocess as sp

from os.path import basename
from dataclasses import dataclass, field
from sys import exit
from typing import Generator

from helpers import extract_archive, persist_to_file, abort, parse_version, platform, architecture
from paths import INSTALL_PATH, CACHE_DIR, SAVE_DIR, TMP_DIR
from downloader import download_app
import desktop




os.makedirs(CACHE_DIR,exist_ok=True)
os.makedirs(SAVE_DIR,exist_ok=True)



def _version(app_path: str):
    # check=True to check for exit error
    return sp.run([app_path, '--version'], check=False, stdout=sp.PIPE).stdout\
             .decode('utf-8')\
             .strip()

def get_current_version() -> str:
    if not os.path.isfile(INSTALL_PATH):
        return ''
    return _version(INSTALL_PATH)


@persist_to_file(CACHE_DIR + 'cache.dat')
def get_version(app_path: str) -> str:
    return _version(app_path)


def get_installed_apps() -> Generator[str, None, None]:
    with os.scandir(SAVE_DIR) as it:
        for file in it:
            yield file.name


def get_installed_versions() -> Generator[str, None, None]:
    for app in get_installed_apps():
        yield get_version(os.path.join(SAVE_DIR, app))


def is_valid_app(app_path: str) -> bool:
    try:
        get_version(app_path)
    except:
        Warning(f'Cannot get Godot version from {basename(app_path)}')
        return False
    return True




@dataclass
class GodotApp:
    path: str
    version: str = field(init=False)

    def __post_init__(self):
        self.version = self._get_version()

    def _get_version(self) -> str:
        return get_version(self.path)

    def install(self, project=False):
        """Make app the system Godot (from CLI and desktop)"""
        if project:
            # define as app for the current directory
            with open('.gvm', 'w') as version_file:
                version_file.write(self.version)
            print(f'Using {self.version} in project folder {os.getcwd()}')
        else:
            # install as system app
            shutil.copyfile(self.path, INSTALL_PATH)
            desktop.create_shortcut(INSTALL_PATH)
            print(f'Using {self.version} ({INSTALL_PATH})')

    def run(self):
        print(f'Launching {self.version}')
        sp.Popen([self.path, '-e'], stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    def __gt__(self, other):
        return self.version > other.version

    def __lt__(self, other):
        return self.version < other.version

    def __eq__(self, other):
        return self.version == other.version

    def __ne__(self, other):
        return self.version != other.version



class AppManager:
    def __init__(self):
        self.apps: list[GodotApp] = [GodotApp(path) 
                                     for path in self.list_save_dir()
                                     if is_valid_app(path)]
        self.apps.sort(reverse=True)


    def list_save_dir(self) -> list[str]:
        return [os.path.join(SAVE_DIR, path) for path in os.listdir(SAVE_DIR)]


    def add(self, godot_file: str) -> GodotApp:
        # TODO: 
        #       - support multiple kind of arguments (version, version number ...)
        #       - check app is already managed
        return self._add_archive(godot_file)


    def _add_archive(self, godot_file: str) -> GodotApp:
        """Add Godot app to the managed versions

        If the godot_file is a zip archive downloaded from Godot website,
        it is extracted first
        """
        # extract the zip archive if necessary
        if godot_file.endswith('.zip'):
            godot_file = extract_archive(godot_file, TMP_DIR)

        # make sure the file is executable
        os.chmod(godot_file, os.stat(godot_file).st_mode | 0o111)

        if not is_valid_app(godot_file):
            os.remove(godot_file)
            print(f'{godot_file} is not valid')
            abort()

        # add to the list of managed versions
        file_path = os.path.join(SAVE_DIR,basename(godot_file))
        print(f'Saving a copy to {file_path}')
        os.rename(godot_file, file_path)

        new_app = GodotApp(file_path)
        self.apps.append(new_app)
        return new_app


    @property
    def paths(self) -> list[str]:
        return [app.path for app in self.apps]


    @property
    def versions(self) -> list[str]:
        return [app.version for app in self.apps]


    @property
    def project_version(self) -> str | None:
        local_version = None
        with open('.gvm') as version_file:
            local_version = version_file.read()
        return local_version


    def get_app_from_version(self, version: str) -> GodotApp:
        for app in self.apps:
            if app.version == version:
                return app
        raise LookupError(f'{version} is not installed')


    def install(self, app: str|GodotApp, project=False):
        """Install as system Godot version (project=False) or define as Godot 
           version for use in the current directory (project=True)

           app: path or GodotApp 
        """
        if type(app) is str:
            self.add(app).install(project)
        elif type(app) is GodotApp:
            app.install(project)


    def add_version(self, version: str):
        version_number, pre_release, mono = parse_version(version)
        archive = download_app(version_number,
                               prerelease=pre_release,
                               system=platform(),
                               mono=mono,
                               architecture=architecture())
        self.add(archive)


    def remove(self, app: GodotApp):
        os.remove(app.path)
        print(f'Removed {app.version}')
        exit()


    def run_system_version(self):
        current_version = get_current_version()
        if current_version == '':
            print('System version is not defined')
            abort()
        system_app = self.get_app_from_version(current_version)
        system_app.run()


    def run_project_version(self):
        if self.project_version is not None:
            project_app = self.get_app_from_version(self.project_version)
            project_app.run()


