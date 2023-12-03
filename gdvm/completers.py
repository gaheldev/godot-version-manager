import os
from argcomplete.completers import ChoicesCompleter

from .downloader import downloader
from . import manager
from .helpers import FILE_SEP



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



class GodotReleasesCompleter:
    def __call__(self, prefix, parsed_args, **kwargs):
        for name in downloader.release_names(parsed_args.version):
            yield name



class InstalledVersionsCompleter():
    def __init__(self, argument:str=''):
        self.installed = manager.installed_versions()
        self.argument = argument

    def __call__(self, prefix, parsed_args, **kwargs):
        for target in self.installed:
            if self.argument:
                if target in vars(parsed_args)[self.argument]:
                    continue
            if target.startswith(prefix):
                yield target
