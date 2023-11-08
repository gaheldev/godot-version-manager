import pytest
from gdvm.downloader.tuxfamily import TuxfamilyRemote as Remote



remote = Remote()


@pytest.mark.online
def test_is_supported_version_number():
    valid_versions = ['3.1', '4.4.9', '3.0', '3.12', '3.10.13', '4.0.1']
    for valid in valid_versions:
        assert remote._is_supported_version_number(valid)==True, f'{valid} should be a supported version number'

    invalid_versions = ['3', '4', '2.0', '1.12', '3.-1', '5.0.1']
    for invalid in invalid_versions:
        assert remote._is_supported_version_number(invalid)==False, f'{invalid} should not be a supported version number'

