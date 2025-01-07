import os
from argcomplete.completers import ChoicesCompleter
from typing import Callable

from .downloader import downloader
from . import manager
from .helpers import FILE_SEP
from .data import GodotApp



class FilteredFilesCompleter():
    def __init__(self, predicate):
        """
        Create the completer

        A predicate accepts as its only argument a candidate path and either
        accepts it or rejects it.
        """
        assert predicate, "Expected a callable predicate"
        self.predicate = predicate

    def __call__(self, prefix, **kwargs):
        target_dir = os.path.dirname(prefix)
        try:
            names = os.listdir(target_dir or ".")
        except Exception:
            return  # empty iterator
        incomplete_part = os.path.basename(prefix)
        # Iterate on target_dir entries and filter on given predicate
        for name in names:
            if not name.startswith(incomplete_part):
                continue
            candidate = os.path.join(target_dir, name)
            if not self.predicate(candidate):
                continue
            yield candidate + FILE_SEP if os.path.isdir(candidate) else candidate



class GodotVersionNumbersCompleter(ChoicesCompleter):
    def __init__(self):
        super().__init__(downloader.version_numbers())

    def __call__(self, **kwargs):
        return super().__call__(**kwargs)



class GodotVersionsCompleter(ChoicesCompleter):
    def __init__(self):
        self.versions = downloader.version_numbers()
        self.versions_and_release = downloader.version_numbers_with_release()

    def __call__(self, prefix, parsed_args, **kwargs):
        versions = self.versions
        if '-' in prefix:
            versions = self.versions_and_release

        for version in versions:
            if version.startswith(prefix):
                yield version



class GodotReleasesCompleter:
    def __call__(self, prefix, parsed_args, **kwargs):
        if not parsed_args.versions:
            return

        if len(parsed_args.versions) > 1:
            yield 'latest'
            return

        version = parsed_args.versions[0]

        if '*' in version or (prefix != '' and 'latest'.startswith(prefix)):
            yield 'latest'
            return

        for name in downloader.release_names(version):
            yield name



class InstalledVersionsCompleter():
    def __init__(self,
                 argument:str='',
                 filter:Callable[[GodotApp], bool]=(lambda x: True),
                 ):
        self.installed = manager.installed_apps()
        self.argument = argument # parsed_args argument to complete for
        self.filter = filter # returns a boolean to filter which version are completed

    def __call__(self, prefix, parsed_args, **kwargs):
        for target in self.installed:
            if not self.filter(target):
                continue

            if self.argument:
                if target.short_version in vars(parsed_args)[self.argument]:
                    continue

            if target.short_version.startswith(prefix):
                yield target.short_version
