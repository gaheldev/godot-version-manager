from gdvm.helpers import parse_version


def test_parse_version():
    test = {'3.0.1.stable.blabla.5t045t3': ('3.0.1', 'stable', False),
            '4.5.rc1.blabla.mono.sdlgs': ('4.5', 'rc1', True),
            '4.52.dev19.blablasdlgs': ('4.52', 'dev19', False),
            '3.12.100.alpha.blablasdlgs': ('3.12.100', 'alpha', False),
            }

    for version in test.keys():
        assert parse_version(version) == test[version]
