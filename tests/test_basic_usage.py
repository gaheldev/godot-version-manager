from gdvm import manager as m
from gdvm.helpers import platform

import os


app_manager = m.AppManager()

fake_godot_zip = os.path.join('tests', 'fake_godot.zip')

try:
    app = app_manager.add(fake_godot_zip)
except:
    app = None




def test_add_from_zip():
    # Skip this test on windows:
    # data._version : fake_godot bash script isn't run properly and ruins the test
    # but we suspect a real godot executable works fine
    if platform() == 'windows':
        return
    
    assert isinstance(app, m.GodotApp) == True

    if isinstance(app, m.GodotApp):
        assert app.version == '3.42.7.stable.official.666aa6aa'
        assert app.mono == False


def test_list():
    # Skip this test on windows:
    # data._version : fake_godot bash script isn't run properly and ruins the test
    # but we suspect a real godot executable works fine
    if platform() == 'windows':
        return
    
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
