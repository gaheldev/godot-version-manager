import os
from typing import Generator
from abc import abstractmethod

from ..helpers import download



class AbstractRemote:

    @property
    @abstractmethod
    def version_numbers(self) -> Generator[str, None, None]:
        pass


    @abstractmethod
    def prerelease_names(self, version: str) -> Generator[str, None, None]:
        pass


    @abstractmethod
    def latest_release(self, version:str) -> str:
        pass


    @abstractmethod
    def release_names(self, version: str) -> Generator[str, None, None]:
        pass


    def latest_stable_version_number(self) -> str:
        for v in self.version_numbers:
            if self.latest_release(v) == 'stable':
                return v



    def download_app(self,
                     version_number: str,
                     save_path: str,
                     system='linux',
                     architecture='64',
                     mono=False,
                     release='stable') -> str:
        app_links = self._app_links(version_number, mono=mono, release=release)
        matching_links = []
        for link in app_links:
            if self.app_name_matches(link, system, architecture, mono=mono):
                matching_links.append(link)

        if len(matching_links) == 0:
            raise LookupError('App not found in repository')
        elif len(matching_links) > 1:
            raise LookupError('Too many correponding apps, probable parsing error')

        link = matching_links[0]
        download_path = os.path.join(save_path, os.path.basename(link))

        print(f'Downloading {link}')

        download(link, out=download_path)
        print()

        return download_path



    @abstractmethod
    def release_page(self,
                     version_number: str,
                     release: str,
                     mono: bool) -> str:
        pass



    @abstractmethod
    def _app_links(self,
                   version_number: str,
                   mono=False,
                   release='stable') -> list[str]:
        pass



    def _is_app(self, href: str) -> bool:
        return href.endswith('.zip')



    def short_name(self,
                   version_number: str,
                   release: str) -> str:
        return f'{version_number}-{release}'



    def app_name_matches(self,
                         name: str,
                         system,
                         architecture,
                         mono=False):

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
                if architecture == '64':
                    # arch=64 shouldn't match 'arm64'
                    if 'arm64' in name:
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

