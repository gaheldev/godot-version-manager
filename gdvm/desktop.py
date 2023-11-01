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


        case 'osx':
            # TODO:
            # create DESKTOP_PATH
            # copy godot exe to INSTALL_PATH
            # need to copy godot bin to ~/.local/bin/ too ?
            # copy godot.icns to DESKTOP_PATH/Contents/Resources/  (store godot.icns in '~/Library/Application Support/gdvm/ ?)
            # /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "DESKTOP_PATH"
            raise Exception('desktop shortcut not implemented for osx')


        case 'windows':
            raise Exception('desktop shortcut not implemented for windows')
                


