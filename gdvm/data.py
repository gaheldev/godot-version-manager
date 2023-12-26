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


def short_version(long_version: str) -> str:
    number, release, mono = parse_version(long_version)
    mono_suffix = '.mono' if mono else ''
    return f'{number}-{release}{mono_suffix}'



def current_system_version() -> str:
    if not os.path.isfile(INSTALL_PATH):
        return ''
    long_version = _version(INSTALL_PATH)
    return short_version(long_version)



@persist_to_file(os.path.join(CACHE_DIR, 'versions.dat'))
def version(app_path: str) -> str:
    return _version(app_path)



def get_mono_app(mono_dir: str) -> str:
    """ mono_dir is the path to the folder extracted from mono release

        return: path to the mono executable app
    """
    app = app_path_from(mono_dir)
    if not app:
        raise Exception(f'mono app not found in {mono_dir}')
    else:
        return app



def app_path_from(dir: str) -> str:
    """ dir is the path to the folder supposed to contain a Godot binary

        return: path to the executable app
    """
    if os.path.isfile(dir):
        return ''
    for f in os.scandir(dir):
        if f.is_file() and ('Godot_v' in f.name):
            return f.path
    else:
        return ''



@dataclass
class GodotApp:
    path: str
    version: str = field(init=False)
    mono: bool = field(init=False)

    def __post_init__(self):
        self.dir = os.path.dirname(self.path)
        self.version = self._version()
        self.short_version = short_version(self.version)
        number, release, mono = parse_version(self.version)
        self.version_number = number
        self.release = release
        self.mono = mono

    def _version(self) -> str:
        return version(self.path)

    def install(self, system=False):
        """Make app the system Godot (from CLI and desktop)"""
        if system:
            # install as system app
            if os.path.isfile(INSTALL_PATH):
                os.remove(INSTALL_PATH)

            os.symlink(self.path, INSTALL_PATH)
            desktop.create_shortcut(INSTALL_PATH)
            print(f'Using {self.version} ({INSTALL_PATH})')

        else:
            # define as app for the current directory
            with open('.godotversion', 'wb') as version_file:
                encoded_version = f'{self.version}\n'.encode('UTF-8') # encode to binary literals to write \n
                version_file.write(encoded_version)
            print(f'Using {self.version} in project folder {os.getcwd()}')

    def run(self):
        print(f'Launching {self.version}')
        sp.Popen([self.path, '-e'], stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    def remove(self):
        shutil.rmtree(os.path.dirname(self.path))

    @property
    def selfcontain(self):
        # return ._sc_ file or _sc_ file exists
        for f in os.scandir(self.dir):
            if f.name == '._sc_' or f.name == '_sc_':
                    return True
        return False

    @selfcontain.setter
    def selfcontain(self, value):
        if value == self.selfcontain: # nothing to do
            return

        sc_file_path = os.path.join(self.dir, '._sc_')
        if value:
            # create empty ._sc_ file if it doesn't exist
            open(sc_file_path, 'a').close()
            print(f'self contained {self.short_version}')
        else:
            os.remove(sc_file_path)
            print(f'shared config of {self.short_version}')


    def __gt__(self, other):
        return self.version > other.version

    def __lt__(self, other):
        return self.version < other.version

    def __eq__(self, other):
        return self.version == other.version

    def __ne__(self, other):
        return self.version != other.version
