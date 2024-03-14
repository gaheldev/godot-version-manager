import subprocess as sp
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

    case 'windows':
        # Needed because expanduser('~/Desktop') is not always desktop on windows
        user_desktop_path = sp.run(
            ['pwsh', '-C',
            '[System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)'],
            check=False, stdout=sp.PIPE).stdout.decode('utf-8').strip()

        INSTALL_PATH = expanduser('~/AppData/Local/bin/godot')
        DESKTOP_PATH = join(user_desktop_path, 'Godot.lnk')
        APP_DIR = expanduser('~/AppData/Local/Programs/godot-version-manager/apps/')
        CACHE_DIR = expanduser('~/AppData/Local/Programs/godot-version-manager/cache/')
        VERSIONS_PATH = join(CACHE_DIR, 'available_versions.yml')
        LAST_SYNCED_PATH = join(CACHE_DIR, 'last_synced')
        TMP_DIR = expanduser('~/AppData/Local/Temp')

    case _ as platform_name:
        raise NotImplementedError(f'Unsupported platform: {platform_name}')
