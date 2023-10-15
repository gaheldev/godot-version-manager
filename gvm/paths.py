from os.path import expanduser
from .helpers import platform



match platform():
    case 'linux':
        INSTALL_PATH = expanduser('~/.local/bin/godot')
        DESKTOP_PATH = expanduser('~/.local/share/applications/godot.desktop')
        APP_DIR = expanduser('~/.local/share/godot-version-manager/apps/')
        CACHE_DIR = expanduser('~/.cache/godot-version-manager/')
        TMP_DIR = '/tmp/'

    case _ as platform_name:
        raise NotImplementedError(f'Unsupported platform: {platform_name}')
