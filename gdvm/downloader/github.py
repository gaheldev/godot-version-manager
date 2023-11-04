import requests
from bs4 import BeautifulSoup
import os
from typing import Generator
import re

from ..paths import VERSIONS_PATH
from ..helpers import urljoin
from .godotwebsite import VersionParser
from .abstractremote import AbstractRemote



class GithubRemote(AbstractRemote):

    def __init__(self):
        # TODO: this is way too slow, should only run after parsing download
        self.website_builds = VersionParser()

        self.RELEASE_REPO = 'https://github.com/godotengine/godot/releases/download/'
        self.PRERELEASE_REPO = 'https://github.com/godotengine/godot-builds/releases/download/'



    @property
    def version_numbers(self) -> Generator[str, None, None]:
        for v in self.website_builds.versions:
            yield v.name



    def prerelease_names(self, version: str) -> Generator[str, None, None]:
        v = self.website_builds[version]
        if v is not None:
            return v.prereleases
        else:
            raise LookupError(f'version {v} is not found in {VERSIONS_PATH}')



    def release_names(self, version: str) -> Generator[str, None, None]:
        v = self.website_builds[version]
        if v is not None:
            return v.releases
        else:
            raise LookupError(f'version {v} is not found in {VERSIONS_PATH}')



    def release_page(self,
                     version_number: str,
                     release: str,
                     mono: bool) -> str:
        if release == 'stable':
            repo = 'https://github.com/godotengine/godot/releases/expanded_assets/'
        else:
            repo = 'https://github.com/godotengine/godot-builds/releases/expanded_assets/'
        return f'{repo}{self.short_name(version_number,release)}'



    def download_link(self,
                      version_name,
                      version_number: str,
                      release: str) -> str:
        if release == 'stable':
            repo = self.RELEASE_REPO
        else:
            repo = self.PRERELEASE_REPO
        short_version = self.short_name(version_number, release)
        return urljoin(repo, short_version, version_name)



    def _app_links(self,
                   version_number: str,
                   mono=False,
                   release='stable') -> list[str]:
        repo = self.release_page(version_number, release, mono)

        page = requests.get(repo)
        soup = BeautifulSoup(page.content, 'lxml')

        hrefs_tags = soup.find_all('a', {'href': re.compile(r'Godot.*\.zip')})

        release_names = [os.path.basename(tag.get('href')) for tag in hrefs_tags]

        app_links = [ self.download_link(release_name, version_number, release)
                     for release_name in release_names
                     if self._is_app(release_name)]

        return app_links


