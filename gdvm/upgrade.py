import requests
from bs4 import BeautifulSoup
import wget
import os
from shutil import unpack_archive
import subprocess as sp
import re

from .paths import TMP_DIR
from . import __version__
from .helpers import platform



ARCHIVE_REPO = 'https://github.com/gaheldev/godot-version-manager/releases/latest'


match platform():
    case 'linux':
        release_zip = 'gdvm_linux.zip'
    case _ as platform_name:
        raise NotImplementedError(f'Unsupported platform: {platform_name}')



def latest_release() -> str:
    """ version name of the latest release available """
    page = requests.get(ARCHIVE_REPO)
    soup = BeautifulSoup(page.content, 'html.parser')
    release_regex = re.compile(r'v\d+\.\d+\.\d+')
    version = release_regex.findall(soup.title.string)[0]
    if version is None:
        raise Exception('last gdvm release version not found')
    return version


def release_link(version: str) -> str:
    return f'https://github.com/gaheldev/godot-version-manager/releases/download/{version}/{release_zip}'


def is_more_recent_than_current(version: str):
    class Version:
        def __init__(self, version):
            self.version = version
            self.version_number = version[1:].split('-')[0] # remove 'v' and dev suffix
            sub_versions = self.version_number.split('.')
            self.major = int(sub_versions[0])
            self.minor = int(sub_versions[1])
            self.patch = int(sub_versions[2])

    cur = Version(__version__)
    new = Version(version)

    if cur.major != new.major:
        return new.major > cur.major
    if cur.minor != new.minor:
        return new.minor > cur.minor
    if cur.patch != new.patch:
        return new.patch > cur.patch
    return False # if the version is the same
    



def upgrade(version: str):
    link = release_link(version)
    archive = os.path.join(TMP_DIR, os.path.basename(link))
    try:
        wget.download(link, out=archive)
        print()
    except KeyboardInterrupt:
        import sys
        print()
        print("Aborting...")
        sys.exit()

    unpack_archive(archive, TMP_DIR)
    extracted = os.path.join(TMP_DIR, 'gdvm')

    # make script executable
    os.chdir(extracted)
    install_script = os.path.join(extracted, 'install')
    os.chmod(install_script, os.stat(install_script).st_mode | 0o111)

    sp.run([install_script, '--force'], check=True)
