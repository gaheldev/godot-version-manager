pip install -r requirements.txt
pyinstaller -F main.py -n gdvm

sudo cp dist/gdvm ~/.local/bin/
register-python-argcomplete gdvm > gdvm.completion
sudo cp gdvm.completion /usr/share/bash-completion/completions/gdvm

sudo cp godot.png /usr/share/pixmaps/
rm -r ~/.cache/gdvm 2> /dev/null || true
