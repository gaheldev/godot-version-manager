import subprocess as sp
import os

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
            if os.path.isfile(DESKTOP_PATH):
                os.remove(DESKTOP_PATH)

            create_shortcut_command = f"""#!pwsh
                $shell = New-Object -comObject WScript.Shell
                $shortcut = $shell.CreateShortcut("{DESKTOP_PATH}")
                $shortcut.TargetPath = "{path}"
                $shortcut.Save()
            """
            sp.run(['pwsh', '-C', create_shortcut_command])
