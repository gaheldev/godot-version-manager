import os
# from urllib.request import urlopen
import yaml
from typing import Generator
import wget
from datetime import date

from ..paths import VERSIONS_PATH, LAST_SYNCED_PATH



# TODO: download versions last modification of VERSIONS_PATH is from less than a day? or if no network ?
REMOTE_VERSIONS_FILE = 'https://raw.githubusercontent.com/godotengine/godot-website/master/_data/versions.yml'


def sync():
    print('Getting latest releases...')
    wget.download(REMOTE_VERSIONS_FILE, out=VERSIONS_PATH)
    print()
    with open(LAST_SYNCED_PATH, 'w') as f:
        f.write(date.today().isoformat())



def days_since_synced() -> int:
    if not os.path.isfile(LAST_SYNCED_PATH):
        sync()

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
            yield r

    @property
    def prereleases(self) -> Generator[str, None, None]:
        if not self.is_stable:
            yield self.latest
        for r in self.dic['releases']:
            yield r['name']



class VersionParser():

    remote = REMOTE_VERSIONS_FILE
    cache = VERSIONS_PATH

    def __init__(self):
        if days_since_synced() >= 1:
            sync()

        with open(self.cache) as stream:
            self.yaml = yaml.safe_load(stream)

        # with urlopen(self.remote) as stream:
        #     self.yaml = yaml.safe_load(stream)
    
    @property
    def versions(self) -> Generator[Version, None, None]:
        for v in self.yaml:
            yield Version(v)
                
    def __getitem__(self, version: str) -> Version:
        for v in self.yaml:
            if v['name'] == version:
                return Version(v)
        raise KeyError
                
