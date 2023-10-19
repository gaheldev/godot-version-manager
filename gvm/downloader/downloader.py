from typing import Generator

from . import tuxfamily as tf
from ..paths import TMP_DIR





def get_version_numbers() -> Generator[str, None, None]:
    return tf.get_version_numbers()


def get_prerelease_names(version: str) -> Generator[str, None, None]:
    return tf.get_prerelease_names(version)


def get_release_names(version: str) -> Generator[str, None, None]:
    return tf.get_release_names(version)


def download_app(version_number: str,
                 system='linux',
                 architecture='64',
                 mono=False,
                 release='stable',
                 dl_path=TMP_DIR) -> str:

    return tf.download_app(version_number,
                           dl_path,
                           system=system,
                           architecture=architecture,
                           mono=mono,
                           release=release)
