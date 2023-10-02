from os.path import expanduser
from helpers import platform



match platform():
    case 'linux':
        INSTALL_PATH = expanduser('~/.local/bin/godot')
        DESKTOP_PATH = expanduser('~/.local/share/applications/godot.desktop')
        CACHE_DIR = expanduser('~/.godot-version-manager/')
        SAVE_DIR = expanduser('~/.godot/')
        TMP_DIR = '/tmp/'

    case _:
        raise NotImplemented(f'Unsupported platform: {_}')
