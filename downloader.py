import requests
import wget
from bs4 import BeautifulSoup
import re
import os
from typing import Generator


# Only support godot 3 and 4 stable for now (not mono, rc or beta)
#
# Tree of the repo:
#   3.x/
#       mono/
#       beta/
#       rcx/
#       Godot_v3.x-stable_{platform}.zip
#
#   4.x/
#       mono/
#       beta/
#       rcx/
#       Godot_v4.x-stable_{platform}.zip
#
#
#
#
# [ ] Linux:
#       [ ] v3: {platform} -> x11.32 | x11.64
#       [ ] v4: {platform} -> linux.x86_32 | linux.x86_64
#
# [ ] Windows:
#       [ ] v3: {platform} -> win32.exe | win64.exe
#       [ ] v4: {platform} -> win32.exe | win64.exe

ARCHIVE_REPO = 'https://downloads.tuxfamily.org/godotengine/'
TMP = '/tmp'


# matches 3.x, 4.x, 3.x.x.x ...
regex_version_number = re.compile(r'[3-4](\.\d)+')

def is_supported_version_number(s: str) -> bool:
    return regex_version_number.match(s) is not None

def is_version_dir(dir_name: str) -> bool:
    return is_supported_version_number(dir_name.rstrip('/'))

def is_prerelease_dir(dir_name: str) -> bool:
    return ('rc' in dir_name) or ('alpha' in dir_name) or ('beta' in dir_name)

def is_app(href: str) -> bool:
    return href.endswith('.zip')


def get_version_numbers() -> Generator[str, None, None]:
    page = requests.get(ARCHIVE_REPO)
    soup = BeautifulSoup(page.content, 'html.parser')
    # get all hyperlinks from table which are root directories in ARCHIVE_REPO
    root_dirs_tags = soup.select('table')[0].tbody.find_all('a')
    for tag in root_dirs_tags:
        root_dir = tag.get('href')
        if is_version_dir(root_dir):
            yield root_dir.rstrip('/')


def get_prerelease_names(version: str) -> Generator[str, None, None]:
    repo = os.path.join(ARCHIVE_REPO, version)
    page = requests.get(repo)
    soup = BeautifulSoup(page.content, 'html.parser')
    # get all hyperlinks from table
    links_tags = soup.select('table')[0].tbody.find_all('a')
    for tag in links_tags:
        link = tag.get('href')
        if is_prerelease_dir(link):
            yield link.rstrip('/')



def app_name_matches(name: str, system, architecture):
    match system:
        case 'linux':
            if 'linux' not in name:
                if 'x11' not in name:
                    return False
            if 'headless' in name or 'server' in name:
                return False
            if architecture not in name:
                return False

        case 'windows':
            if 'win' not in name:
                return False
            if architecture not in name:
                return False

        case 'osx':
            if ('osx' not in name) and ('macos' not in name):
                return False

        case 'web':
            raise NotImplementedError(f'unsupported system: {system}')

        case 'android':
            raise NotImplementedError(f'unsupported system: {system}')

        case 'linux-server':
            raise NotImplementedError(f'unsupported system: {system}')

        case 'linux-headless':
            raise NotImplementedError(f'unsupported system: {system}')

        case _:
            return False

    return True


def download_app(version_number: str,
                 system='linux',
                 architecture='64',
                 mono=False,
                 prerelease='') -> str:
    app_links = get_app_links(version_number, mono=mono, prerelease=prerelease)
    matching_links = []
    for link in app_links:
        if app_name_matches(link, system, architecture):
            matching_links.append(link)

    if len(matching_links) == 0:
        raise LookupError('App not found in repository')
    elif len(matching_links) > 1:
        raise LookupError('Too many correponding apps, probable parsing error')

    link = matching_links[0]
    download_path = os.path.join(TMP,os.path.basename(link))
    print(f'Downloading {link}')
    wget.download(link, out=download_path)
    print()
    return download_path



def get_app_links(version_number: str, mono=False, prerelease='') -> list[str]:
    repo = os.path.join(ARCHIVE_REPO, version_number)
    if prerelease != '':
        repo = os.path.join(repo, prerelease)
    if mono:
        repo = os.path.join(repo, 'mono')

    page = requests.get(repo)
    soup = BeautifulSoup(page.content, 'html.parser')
    # get all hyperlinks in the table, which include downloadable Godot apps
    hrefs_tags = soup.select('table')[0].tbody.find_all('a')
    hrefs = [tag.get('href') for tag in hrefs_tags]
    app_links = [os.path.join(repo,href) for href in hrefs if is_app(href)]
    return app_links


