import os
# from urllib.request import urlopen
import yaml
from typing import Generator
from datetime import date
from functools import cached_property

from ..paths import CACHE_DIR, VERSIONS_PATH, LAST_SYNCED_PATH
from ..helpers import download



os.makedirs(CACHE_DIR, exist_ok=True)

# TODO: download versions last modification of VERSIONS_PATH is from less than a day? or if no network ?
REMOTE_VERSIONS_FILE = 'https://raw.githubusercontent.com/godotengine/godot-website/master/_data/versions.yml'



def sync():
    print('Getting available Godot releases...')
    download(REMOTE_VERSIONS_FILE, out=VERSIONS_PATH)

    with open(LAST_SYNCED_PATH, 'w') as f:
        f.write(date.today().isoformat())



def days_since_synced() -> int:
    if not os.path.isfile(LAST_SYNCED_PATH):
        raise FileNotFoundError('Fix by running: gdvm sync')

    today = date.today()
    with open(LAST_SYNCED_PATH) as f:
        last_synced = date.fromisoformat(f.read())
    return (today - last_synced).days
        


class Version():
    def __init__(self, dic):
        self.name = dic['name']
        self.latest = dic['flavor']
        self.is_stable = self.latest == 'stable'
        self.dic = dic
        
    @property
    def releases(self) -> Generator[str, None, None]:
        yield self.latest
        for r in self.prereleases:
            if r != self.latest:
                yield r

    @property
    def prereleases(self) -> Generator[str, None, None]:
        if not self.is_stable:
            yield self.latest

        if not 'releases' in self.dic:
            return

        for r in self.dic['releases']:
            yield r['name']



class VersionParser():

    remote = REMOTE_VERSIONS_FILE
    cache = VERSIONS_PATH


    @cached_property
    def _yaml(self):
        if (not os.path.isfile(self.cache)) or (days_since_synced() >= 1):
            sync()

        with open(self.cache) as stream:
            return yaml.safe_load(stream)


    @property
    def versions(self) -> Generator[Version, None, None]:
        for v in self._yaml:
            version = Version(v)
            if int(version.name[0]) >= 3: # only return versions >= 3.0
                yield version
                
    def __getitem__(self, version: str) -> Version:
        for v in self._yaml:
            if v['name'] == version:
                return Version(v)
        raise KeyError
                
