import pytest
from gdvm.downloader import github


@pytest.mark.online
def test_version_parser():
    parser = github.VersionParser()
    assert parser._yaml is not None

    assert parser['4.0'] is not None

    assert parser['3.0'].is_stable == True
