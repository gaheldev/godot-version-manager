from typing import Generator

# from . import tuxfamily as remote
from .github import GithubRemote as Remote
from ..paths import TMP_DIR



remote = Remote()



def get_version_numbers() -> Generator[str, None, None]:
    return remote.version_numbers



def get_prerelease_names(version: str) -> Generator[str, None, None]:
    return remote.prerelease_names(version)



def get_release_names(version: str) -> Generator[str, None, None]:
    return remote.release_names(version)



def download_app(version_number: str,
                 system='linux',
                 architecture='64',
                 mono=False,
                 release='stable',
                 dl_path=TMP_DIR) -> str:

    return remote.download_app(version_number,
                               dl_path,
                               system=system,
                               architecture=architecture,
                               mono=mono,
                               release=release)
