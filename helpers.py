from os.path import basename, splitext, isfile, join
import shutil
from sys import exit
from platform import system, machine
import json
import re
from typing import Tuple




def extract_archive(file: str, to_dir: str) -> str:
    """Extracts Godot archive to /tmp and return extracted file path"""
    shutil.unpack_archive(file, to_dir)
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



def architecture() -> str:
    if '32' in machine():
        return '32'
    else:
        return '64'



def parse_version(version: str) -> Tuple[str, str, bool]:
    nb = re.compile(r'^[1-4](\.\d)+')
    version_number = nb.match(version)[0]

    pre = re.compile(r'.*(?P<prerelease>alpha\d?|beta\d?|rc\d?).*')
    m = pre.match(version)
    pre_release = m.group('prerelease') if m is not None else ''

    mono = False
    if 'mono' in version:
        mono = True

    return version_number, pre_release, mono



def persist_to_file(file_name):

    def decorator(original_func):
        try:
            cache = json.load(open(file_name, 'r'))
        except (IOError, ValueError):
            cache = {}

        def new_func(param):
            if param not in cache:
                cache[param] = original_func(param)
                json.dump(cache, open(file_name, 'w'))
            return cache[param]

        return new_func

    return decorator

