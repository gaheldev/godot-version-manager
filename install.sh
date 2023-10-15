pip install -r requirements.txt
pyinstaller -F main.py -n gvm

sudo cp dist/gvm ~/.local/bin/
register-python-argcomplete gvm > gvm.completion
sudo cp gvm.completion /usr/share/bash-completion/completions/gvm

sudo cp godot.png /usr/share/pixmaps/
rm ~/.godot-version-manager/cache.dat 2> /dev/null || true
