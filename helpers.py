import subprocess as sp
from os.path import basename, splitext, isfile, join
from sys import exit
from platform import system
import json




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

