import os
from argcomplete.completers import ChoicesCompleter

from .downloader import downloader
from . import manager



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
            yield candidate + "/" if os.path.isdir(candidate) else candidate



class GodotVersionNumbersCompleter(ChoicesCompleter):
    def __init__(self):
        super().__init__(downloader.version_numbers())

    def __call__(self, **kwargs):
        return super().__call__(**kwargs)



class GodotReleasesCompleter:
    def __call__(self, prefix, parsed_args, **kwargs):
        for name in downloader.release_names(parsed_args.version):
            yield name



class InstalledVersionsCompleter(ChoicesCompleter):
    def __init__(self):
        super().__init__(manager.installed_versions())

    def __call__(self, **kwargs):
        return super().__call__(**kwargs)
