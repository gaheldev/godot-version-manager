from gdvm import manager as m
import os



app_manager = m.AppManager()

fake_godot_zip = os.path.join('tests', 'fake_godot.zip')

try:
    app = app_manager.add(fake_godot_zip)
except:
    app = None




def test_add_from_zip():
    assert isinstance(app, m.GodotApp) == True

    if isinstance(app, m.GodotApp):
        assert app.version == '3.42.7.stable.official.666aa6aa'
        assert app.mono == False


# TODO
def test_list():
    pass


# TODO
def test_use_local():
    pass


def test_remove():
    if isinstance(app, m.GodotApp):
        app.remove()
    assert os.path.isfile(app.path) == False
