import subprocess as sp
from os.path import basename, splitext


def extract_archive(file: str) -> str:
    """Extracts Godot archive to /tmp and return extracted file path"""
    sp.run(['unzip', file, '-d', '/tmp'])
    return '/tmp/' + basename(splitext(file)[0])


def abort():
    print('Aborting...')
    exit()
