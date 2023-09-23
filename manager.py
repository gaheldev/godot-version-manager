import os
import subprocess as sp

from os.path import basename, expanduser
from dataclasses import dataclass, field

from helpers import extract_archive
from downloader import download_app



INSTALL_PATH = '/usr/bin/godot'
SAVE_DIR = expanduser('~/.godot/')

os.makedirs(SAVE_DIR,exist_ok=True)




def get_current_version() -> str:
    return get_version(INSTALL_PATH)



def get_version(app_path: str) -> str:
    # check=True to check for exit error
    return sp.run([app_path, '--version'], check=False, stdout=sp.PIPE).stdout\
             .decode('utf-8')\
             .strip()



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
            sp.run(['sudo', 'cp', self.path, INSTALL_PATH])
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


    def add(self, godot_file: str):
        # TODO: 
        #       - support multiple kind of arguments (version, version number ...)
        #       - check app is already managed
        self._add_archive(godot_file)


    def _add_archive(self, godot_file: str):
        """Add Godot app to the managed versions

        If the godot_file is a zip archive downloaded from Godot website,
        it is extracted first
        """
        # extract the zip archive if necessary
        if godot_file.endswith('.zip'):
            godot_file = extract_archive(godot_file)

        if not is_valid_app(godot_file):
            print(f'{godot_file} is not valid')
            return

        # make Godot executable
        sp.run(['chmod', '+x', godot_file])

        # add to the list of managed versions
        print(f'Saving a copy to {SAVE_DIR}{basename(godot_file)}')
        sp.run(['mv', godot_file, SAVE_DIR])

        new_app = GodotApp(os.path.join(SAVE_DIR,basename(godot_file)))
        self.apps.append(new_app)


    @property
    def paths(self) -> list[str]:
        return [app.path for app in self.apps]


    @property
    def versions(self) -> list[str]:
        return [app.version for app in self.apps]


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
            self.add(app)
            GodotApp(app).install(project)
        elif type(app) is GodotApp:
            app.install(project)


    def install_from_repo(self, version: str, system: str, arch: str):
        archive = download_app(version, system, arch)
        self.install(archive)


    def remove(self, app: GodotApp):
        os.remove(app.path)
        print(f'Removed {app.version}')
        exit()


    def run_system_version(self):
        system_app = self.get_app_from_version(get_current_version())
        system_app.run()


    def run_project_version(self):
        with open('.gvm') as version_file:
            local_version = version_file.read()
        project_app = self.get_app_from_version(local_version)
        project_app.run()


