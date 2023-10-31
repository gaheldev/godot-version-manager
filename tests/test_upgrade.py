import re
import pytest

from gdvm import upgrade as up



@pytest.mark.slow
def test_latest_release():
    release_regex = re.compile(r'v\d+\.\d+\.\d+')
    latest = up.latest_release()
    assert (release_regex.match(latest) is not None) == True

def test_is_more_recent_than_current():
    assert up.is_more_recent_than_current('v9345.0999.1-n-blabla') == True


