from gdvm import manager as m
from gdvm.paths import CACHE_DIR

import os



app_manager = m.AppManager()

# cache might interfere with fake godot installations
version_cache = os.path.join(CACHE_DIR, 'versions.dat')
os.remove(version_cache)

fake_godot_zip = os.path.join('tests', 'fake_godot.zip')
try:
    app = app_manager.add(fake_godot_zip)
except:
    app = None



def test_add_from_current_directory():
    # # move fake godot file in cwd
    # os.rename('tests/fake_godot_wd', 'fake_godot_wd')
    os.chdir('tests')
    try:
        app_wd = app_manager.add('fake_godot_wd')
    except:
        app_wd = None
    # finally:
    #     # Use finally so the file is ALWAYS moved back, even if add() raises
    #     if os.path.exists('fake_godot_wd'):
    #         os.rename('fake_godot_wd', 'tests/fake_godot_wd')

    os.chdir('..')

    assert (app_wd is not None) == True
    if app_wd is not None:
        app_manager.remove(app_wd)


def test_add_from_outer_directory():
    fake_godot = os.path.join('tests', 'fake_godot_outer')
    try:
        app_outer = app_manager.add(fake_godot)
    except:
        app_outer = None

    assert (app_outer is not None) == True

    if app_outer is not None:
        app_manager.remove(app_outer)


def test_add_from_zip():
    assert isinstance(app, m.GodotApp) == True

    if isinstance(app, m.GodotApp):
        assert app.version == '3.42.7.stable.official.666aa6aa'
        assert app.mono == False


def test_list():
    assert ('3.42.7-stable' in app_manager.versions) == True
    assert ('not_a_version' in app_manager.versions) == False


def test_use_local():
    if isinstance(app, m.GodotApp):
        os.chdir('tests/')
        app.install(system=False)
        version = ''
        with open('.godotversion') as version_file:
            version = version_file.read().strip()
        assert version == '3.42.7.stable.official.666aa6aa'
        os.remove('.godotversion')
        os.chdir('../')


def test_remove():
    if isinstance(app, m.GodotApp):
        app.remove()
        assert os.path.isfile(app.path) == False
        assert os.path.isdir(os.path.dirname(app.path)) == False
