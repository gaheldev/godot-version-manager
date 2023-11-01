from os.path import expanduser, join
from .helpers import platform



match platform():
    case 'linux':
        INSTALL_PATH = expanduser('~/.local/bin/godot')
        DESKTOP_PATH = expanduser('~/.local/share/applications/godot.desktop')
        APP_DIR = expanduser('~/.local/share/gdvm/apps/')
        CACHE_DIR = expanduser('~/.cache/gdvm/')
        VERSIONS_PATH = join(CACHE_DIR, 'available_versions.yml')
        LAST_SYNCED_PATH = join(CACHE_DIR, 'last_synced')
        TMP_DIR = '/tmp/'

    case 'osx':
        INSTALL_PATH = expanduser('~/Applications/Godot.app/Godot')
        DESKTOP_PATH = expanduser('~/Applications/Godot.app/')
        APP_DIR = expanduser('~/Library/Application Support/gdvm/apps')
        CACHE_DIR = expanduser('~/Library/Caches/gdvm/')
        TMP_DIR = '/tmp/'

    case _ as platform_name:
        raise NotImplementedError(f'Unsupported platform: {platform_name}')
