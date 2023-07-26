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

### Update Godot

Download the desired [godot application](https://godotengine.org/download/) and run
```
godot-version-manager -i <path/to/the/downloaded/file>
```

Both running ```godot``` in the terminal or opening Godot's desktop application will point to the new installed version.
<br> <br/>

### Use an already installed Godot version

```
godot-version-manager -u
```

### Advanced usage

Run ```godot-version-manager -h``` for more informations
