from gdvm import manager as m



# TODO: use made up installed versions
def test_expand_pattern():
    assert list(m.expand_pattern('a')) == ['a']
    assert list(m.expand_pattern('a')) != ['b']

    installed = list(m.installed_versions())
    if len(installed) == 0:
        return

    version = installed[0]
    assert (version in list(m.expand_pattern(version))) == True
    assert (version in list(m.expand_pattern(version[:4] + '*'))) == True

    assert ('another' in list(m.expand_pattern(version)) + ['another']) == True
    assert (version in list(m.expand_pattern(version)) + ['another']) == True
    assert ('nope' in list(m.expand_pattern(version[:4] + '*'))) == False

    if len(installed) < 2:
        return
    assert (installed[1] in list(m.expand_pattern([version[:4] + '*',  installed[1][:4] + '*']))) == True

