# Godot Version Manager for Linux 🐧

Creates a desktop shortcut for godot and provides a script to update Godot version. \
Still requires to download Godot's desired version manually. \
All downloaded versions are saved in ```~/.godot/```


## 🛠️ Installation
```
git clone https://github.com/ZelvStudio/godot-version-manager.git
cd godot-version-manager
chmod +x install.sh
./install.sh
```

## 📝 Usage

Install a new version by downloading the desired [godot application](https://godotengine.org/download/) and running ```godot-version-manager -i <path/to/the/downloaded/file>``` on the zip archive or binary.

Change the currently used Godot version to one of the managed version by running ```godot-version-manager -u```

Run ```godot-version-manager -h``` for more informations
