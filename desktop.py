import subprocess as sp
from os.path import expanduser

from helpers import platform




LINUX_DESKTOP_PATH=expanduser('~/.local/share/applications/godot.desktop')



def create_shortcut(path: str, version=''):
    if version != '':
        version = ' ' + version

    match platform():
        case 'linux':
            with open(LINUX_DESKTOP_PATH, 'w') as f:
                linux_desktop = f"""[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Exec={path}
Name=Godot{version}
Comment=Application for making games
GenericName=Game Engine
Icon=godot
Categories=Development;"""

                f.write(linux_desktop)
                sp.run(['xdg-desktop-menu', 'install', '--novendor', f'{LINUX_DESKTOP_PATH}'])
                


