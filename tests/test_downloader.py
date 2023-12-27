import pytest
from gdvm.downloader import downloader as dl


@pytest.mark.online
def test_latest_stable_version_number():
    v = dl.latest_stable_version_number()
    assert v > '4.1.3' # weak test to make sure latest is indeed recent

