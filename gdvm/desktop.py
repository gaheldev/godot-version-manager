import subprocess as sp

from .helpers import platform
from .paths import DESKTOP_PATH




def create_shortcut(path: str, version=''):
    if version != '':
        version = ' ' + version

    match platform():
        case 'linux':
            with open(DESKTOP_PATH, 'w') as f:
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
                sp.run(['xdg-desktop-menu', 'install', '--novendor', f'{DESKTOP_PATH}'])
        
        case 'windows':
            # TODO : actually implement
            print('Creating shortcut')
                


