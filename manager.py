import os
import subprocess as sp

from os.path import basename, splitext, expanduser
from collections import namedtuple



INSTALL_PATH = '/usr/bin/godot'
SAVE_DIR = expanduser('~/.godot/')

os.makedirs(SAVE_DIR,exist_ok=True)



Choice = namedtuple('Choice', ['id','version','path'])


def extract_archive(file: str) -> str:
    """Extracts Godot archive to /tmp and return extracted file path"""
    sp.run(['unzip', file, '-d', '/tmp'])
    return '/tmp/' + basename(splitext(file)[0])


def add_archive(godot_file: str) -> str:
    """Add Godot app to the managed versions

    If the godot_file is a zip archive downloaded from Godot website,
    it is extracted first
    """
    # extract the zip archive if necessary
    if godot_file.endswith('.zip'):
        godot_file = extract_archive(godot_file)

    # make Godot executable
    sp.run(['chmod', '+x', godot_file])

    # add to the list of managed versions
    print(f'Saving a copy to {SAVE_DIR}{basename(godot_file)}')
    sp.run(['mv', godot_file, SAVE_DIR])
    return os.path.join(SAVE_DIR,basename(godot_file))


def install(godot_file: str):
    """Make godot_file the system Godot (from CLI and desktop)"""
    sp.run(['sudo', 'cp', godot_file, INSTALL_PATH])


def local_install(godot_file: str):
    """Make godot_file the local Godot version in working directory"""
    version = get_version(godot_file)
    with open('.gvm', 'w') as version_file:
        version_file.write(version)


def get_current_version() -> str:
    return get_version('godot')


def get_version(app_path: str) -> str:
    # check=True to check for exit error
    return sp.run([app_path, '--version'], check=False, stdout=sp.PIPE).stdout\
             .decode('utf-8')\
             .strip()


def managed_apps() -> list[str]:
    """Return paths of managed Godot apps"""
    managed_paths = [os.path.join(SAVE_DIR,app) for app in os.listdir(SAVE_DIR)]
    return sorted(managed_paths, reverse=True)


def versions() -> list[str]:
    """Return list of managed Godot versions"""
    return [get_version(app) for app in managed_apps()]


def get_app_from_version(version: str) -> str:
    """Return app path from version

    TODO: refactor so version are stored in an object
    """
    apps = [app for app in managed_apps()]
    for app in apps:
        if get_version(app) == version:
            return app
    raise LookupError(f'{version} is not installed')
