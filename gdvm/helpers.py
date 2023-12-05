from os import remove, chdir
from os.path import basename, splitext, isfile, join, abspath, expanduser
import shutil
from sys import exit
from platform import system, machine
import json
import re
from typing import Tuple
import wget




def extract_archive(file: str, to_dir: str) -> str:
    """ Extracts Godot archive to /tmp and return extracted file path

        Warning: ! loses execute permissions of files
    """
    shutil.unpack_archive(file, to_dir)
    return join(to_dir, basename(splitext(file)[0]))



def abort():
    print('Aborting...')
    exit()



def godotversion_in_cwd() -> bool:
    return isfile(join('.', '.godotversion'))



def current_local_project() -> str | None:
    """ looks for a .godotversion file in the parent tree

        the search is limited to $HOME

        return the path of the first parent folder found with .godotversion file
        return None if no local version exists in the parent tree
    """
    original_dir = abspath('.')
    def reset_cwd():
        chdir(original_dir)

    def cwd():
        return abspath('.')

    stop = abspath(expanduser('~' + FILE_SEP + '..'))
    while cwd() != stop:
        if godotversion_in_cwd():
            local_project = cwd()
            reset_cwd()
            return local_project
        else:
            chdir('..')
    reset_cwd()
    return None





def platform() -> str:
    name = system().lower()
    if name == 'darwin':
        name = 'osx'
    return name


FILE_SEP = '\\' if platform == 'windows' else '/' # first \ escapes the second one


def architecture() -> str:
    if '32' in machine():
        return '32'
    else:
        return '64'



def parse_version(version: str) -> Tuple[str, str, bool]:
    nb = re.compile(r'^[1-4](\.\d+)+')
    version_number = nb.match(version)[0]

    pre = re.compile(r'.*(?P<release>stable|alpha\d*|beta\d*|rc\d*|dev\d*).*')
    m = pre.match(version)

    if m is None:
        raise Exception(f'Could not parse release from version name: {version}')

    release = m.group('release')

    mono = False
    if 'mono' in version:
        mono = True

    return version_number, release, mono



def wildcard_match(pattern:str, target:str):
    return re.fullmatch(re.escape(pattern).replace('\*','.*'), target)



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



def urljoin(*args):
    """ Basic path join for urls that works on both windows and unix
    """
    return '/'.join(arg.rstrip('/') for arg in args)



def urlbasename(url):
    """ Basic path basename for urls that works on both windows and unix
    """
    return url.rstrip('/').split('/')[-1]



def download(link, out=None):
    """ wget wrapper with some safety net

        WARNING: if out exists, it will be removed !!
    """
    try:
        if out is not None:
            if isfile(out):
                remove(out)
            wget.download(link, out=out)
        else:
            wget.download(link)
        print() # newline after wget

    except KeyboardInterrupt:
        import sys
        print()
        print("Aborting...")
        sys.exit()
