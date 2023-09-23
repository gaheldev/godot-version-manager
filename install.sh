pip install -r requirements.txt
pyinstaller -F main.py -n godot-version-manager

sudo cp dist/godot-version-manager /usr/local/bin/
# eval "$(register-python-argcomplete /usr/local/bin/godot-version-manager)"
# eval "$(register-python-argcomplete main.py)" # also register main.py for easier debugging

sudo cp godot.png /usr/share/pixmaps/
sudo cp godot.desktop /usr/share/applications/
xdg-desktop-menu install --novendor /usr/share/applications/godot.desktop
