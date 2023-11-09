import os
import shutil
import subprocess as sp
from dataclasses import dataclass, field

from . import desktop
from .paths import INSTALL_PATH, CACHE_DIR
from .helpers import persist_to_file, parse_version




def _version(app_path: str):
    # check=True to check for exit error
    return sp.run([app_path, '--version'], check=False, stdout=sp.PIPE).stdout\
             .decode('utf-8')\
             .strip()


def _short_version(long_version: str) -> str:
    number, release, mono = parse_version(long_version)
    mono_suffix = '.mono' if mono else ''
    return f'{number}-{release}{mono_suffix}'



def current_system_version() -> str:
    if not os.path.isfile(INSTALL_PATH):
        return ''
    long_version = _version(INSTALL_PATH)
    return _short_version(long_version)



@persist_to_file(os.path.join(CACHE_DIR, 'versions.dat'))
def version(app_path: str) -> str:
    if os.path.isdir(app_path) and 'mono' in app_path:
        return _version(get_mono_app(app_path))
    return _version(app_path)



def get_mono_app(mono_dir: str) -> str:
    """ mono_dir is the path to the folder extracted from mono release

        return: path to the mono executable app
    """
    for f in os.scandir(mono_dir):
        if f.is_file() and ('Godot_v' in f.name):
            return f.path
    raise Exception(f'mono app not found in {mono_dir}')



@dataclass
class GodotApp:
    path: str
    version: str = field(init=False)
    mono: bool = field(init=False)

    def __post_init__(self):
        self.version = self._version()
        self.short_version = _short_version(self.version)
        number, release, mono = parse_version(self.version)
        self.version_number = number
        self.release = release
        self.mono = mono

    def _version(self) -> str:
        return version(self.path)

    def install(self, project=False):
        """Make app the system Godot (from CLI and desktop)"""
        if project:
            # define as app for the current directory
            with open('.godotversion', 'w') as version_file:
                version_file.write(self.version)
            print(f'Using {self.version} in project folder {os.getcwd()}')
        else:
            if self.mono:
                raise NotImplementedError("""Defining as system's default is unsupported for mono builds""")
            # install as system app
            shutil.copy(self.path, INSTALL_PATH)
            desktop.create_shortcut(INSTALL_PATH)
            print(f'Using {self.version} ({INSTALL_PATH})')

    def run(self):
        print(f'Launching {self.version}')
        executable = self.path if not self.mono else get_mono_app(self.path)
        sp.Popen([executable, '-e'], stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    def remove(self):
        if self.mono:
            shutil.rmtree(self.path)
        else:
            os.remove(self.path)


    def __gt__(self, other):
        return self.version > other.version

    def __lt__(self, other):
        return self.version < other.version

    def __eq__(self, other):
        return self.version == other.version

    def __ne__(self, other):
        return self.version != other.version
