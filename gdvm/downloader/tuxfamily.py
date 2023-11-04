import requests
from bs4 import BeautifulSoup
import re
import os
from typing import Generator

from .abstractremote import AbstractRemote


# Supports godot 3 and 4 stable, alpha, beta, rc and dev for standard and mono builds
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


class TuxfamilyRemote(AbstractRemote):

    def __init__(self):
        self.ARCHIVE_REPO = 'https://downloads.tuxfamily.org/godotengine/'

        # matches 3.x, 4.x, 3.x.x.x ...
        self.regex_version_number = re.compile(r'[3-4](\.\d)+')



    def _is_supported_version_number(self, number: str) -> bool:
        return self.regex_version_number.match(number) is not None



    def _is_version_dir(self, dir_name: str) -> bool:
        return self._is_supported_version_number(dir_name.rstrip('/'))



    def _is_prerelease_dir(self, dir_name: str) -> bool:
        return ('rc' in dir_name)\
               or ('alpha' in dir_name)\
               or ('beta' in dir_name)\
               or ('dev' in dir_name)



    @property
    def version_numbers(self) -> Generator[str, None, None]:
        page = requests.get(self.ARCHIVE_REPO)
        soup = BeautifulSoup(page.content, 'lxml')
        # get all hyperlinks from table which are root directories in ARCHIVE_REPO
        root_dirs_tags = soup.select('table')[0].tbody.find_all('a')
        for tag in root_dirs_tags:
            root_dir = tag.get('href')
            if self._is_version_dir(root_dir):
                yield root_dir.rstrip('/')



    def prerelease_names(self, version: str) -> Generator[str, None, None]:
        for link in self.release_names(version):
            if not 'stable' in link:
                yield link



    def release_names(self, version: str) -> Generator[str, None, None]:
        repo = os.path.join(self.ARCHIVE_REPO, version)
        page = requests.get(repo)
        soup = BeautifulSoup(page.content, 'lxml')
        # get all hyperlinks from table
        links_tags = soup.select('table')[0].tbody.find_all('a')

        yielded_stable = False
        for tag in links_tags:
            link = tag.get('href')
            if self._is_prerelease_dir(link):
                yield link.rstrip('/')
            if not yielded_stable:
                if 'stable' in link:
                    yield 'stable'
                    yielded_stable = True



    def release_page(self,
                     version_number: str,
                     release: str,
                     mono: bool) -> str:
        repo = os.path.join(self.ARCHIVE_REPO, version_number)
        if release != 'stable':
            repo = os.path.join(repo, release)
        if mono:
            repo = os.path.join(repo, 'mono')
        return repo


    def _app_links(self,
                   version_number: str,
                   mono=False,
                   release='stable') -> list[str]:
        repo = self.release_page(version_number, release, mono)

        page = requests.get(repo)
        soup = BeautifulSoup(page.content, 'lxml')
        # get all hyperlinks in the table, which include downloadable Godot apps
        hrefs_tags = soup.select('table')[0].tbody.find_all('a')
        hrefs = [tag.get('href') for tag in hrefs_tags]
        app_links = [os.path.join(repo,href) for href in hrefs if self._is_app(href)]
        return app_links


