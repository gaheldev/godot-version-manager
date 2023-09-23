pip install -r requirements.txt
pyinstaller -F main.py -n godot-version-manager

sudo cp dist/godot-version-manager /usr/local/bin/
register-python-argcomplete godot-version-manager > godot-version-manager.completion
sudo cp godot-version-manager.completion /usr/share/bash-completion/completions/godot-version-manager

sudo cp godot.png /usr/share/pixmaps/
sudo cp godot.desktop /usr/share/applications/
xdg-desktop-menu install --novendor /usr/share/applications/godot.desktop
