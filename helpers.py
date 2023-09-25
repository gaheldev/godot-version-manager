import subprocess as sp
from os.path import basename, splitext, isfile, join
from sys import exit
from platform import system


def extract_archive(file: str, to_dir: str) -> str:
    """Extracts Godot archive to /tmp and return extracted file path"""
    sp.run(['unzip', file, '-d', to_dir])
    return join(to_dir, basename(splitext(file)[0]))


def abort():
    print('Aborting...')
    exit()


def gvmfile_in_cwd() -> bool:
    return isfile(join('.', '.gvm'))

def platform() -> str:
    name = system().lower()
    if name == 'darwin':
        name = 'osx'
    return name
