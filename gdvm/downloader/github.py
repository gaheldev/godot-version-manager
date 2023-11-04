import requests
import wget
from bs4 import BeautifulSoup
import os
from typing import Generator
import re

from ..paths import VERSIONS_PATH
from .godotwebsite import VersionParser


RELEASE_REPO = 'https://github.com/godotengine/godot/releases/download/'
PRERELEASE_REPO = 'https://github.com/godotengine/godot-builds/releases/download/'



# TODO: this is way too slow, should only run after parsing download
parser = VersionParser()



def get_version_numbers() -> Generator[str, None, None]:
    for v in parser.versions:
        yield v.name


def get_prerelease_names(version: str) -> Generator[str, None, None]:
    v = parser[version]
    if v is not None:
        return v.prereleases
    else:
        raise LookupError(f'version {v} is not found in {VERSIONS_PATH}')


def get_release_names(version: str) -> Generator[str, None, None]:
    v = parser[version]
    if v is not None:
        return v.releases
    else:
        raise LookupError(f'version {v} is not found in {VERSIONS_PATH}')



# TODO
def _app_name_matches(name: str, system, architecture, mono=False):
    if ('mono' in name) != mono:
        return False

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



# TODO: scrap github to get matching release
def download_app(version_number: str,
                 save_path: str,
                 system='linux',
                 architecture='64',
                 mono=False,
                 release='stable') -> str:
    app_links = _get_app_links(version_number, mono=mono, release=release)
    matching_links = []
    for link in app_links:
        if _app_name_matches(link, system, architecture, mono=mono):
            matching_links.append(link)

    if len(matching_links) == 0:
        raise LookupError('App not found in repository')
    elif len(matching_links) > 1:
        raise LookupError('Too many correponding apps, probable parsing error')

    link = matching_links[0]
    download_path = os.path.join(save_path, os.path.basename(link))
    print(f'Downloading {link}')
    wget.download(link, out=download_path)
    print()
    return download_path



def short_name(version_number: str, release: str) -> str:
    return f'{version_number}-{release}'



def release_page(version_number: str, release: str) -> str:
    if release == 'stable':
        repo = 'https://github.com/godotengine/godot/releases/expanded_assets/'
    else:
        repo = 'https://github.com/godotengine/godot-builds/releases/expanded_assets/'
    return f'{repo}{short_name(version_number,release)}'



def download_link(version_name, version_number: str, release: str) -> str:
    if release == 'stable':
        repo = RELEASE_REPO
    else:
        repo = PRERELEASE_REPO
    short_version = short_name(version_number, release)
    return os.path.join(repo, short_version, version_name)



def _is_app(href: str) -> bool:
    return href.endswith('.zip')



def _get_app_links(version_number: str, mono=False, release='stable') -> list[str]:
    repo = release_page(version_number, release)

    page = requests.get(repo)
    soup = BeautifulSoup(page.content, 'lxml')

    hrefs_tags = soup.find_all('a', {'href': re.compile(r'Godot.*\.zip')})

    release_names = [os.path.basename(tag.get('href')) for tag in hrefs_tags]

    app_links = [download_link(release_name, version_number, release)
                 for release_name in release_names
                 if _is_app(release_name)]

    return app_links


