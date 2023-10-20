# Godot Version Manager

Use `gvm` from the command line to manage the Godot version of your different projects.

<br></br>

> [!WARNING]
> This is currently under development, breaking changes will happen





# ✨ Features

* [x] **download** any release of Godot > 3.0 to the managed versions
* [x] **use** a Godot version per project, trackable by `git`
* [x] **run** the project's version and download it automatically if necessary
* [x] **list**, **remove**, **run** managed versions
* [x] **use** a default system version with desktop shortcut (`godot` in terminal)
* [ ] create desktop shortcuts for multiple versions
* [ ] Notify about new available versions
* [x] **add** a Godot binary or archive to managed versions


**supported systems:**
* [x] linux 🐧
* [ ] windows 🪟 (incoming)
* [ ] macos 🍎 (shouldn't be hard)
* [ ] android

<br></br>




# 🛠️ Installation

#### Requirements

This has been developped with `python3.11`, it does not work with older versions of Python 3. If necessary, install it from your package manager as well as `pip` for Python 3.

<!--- Seems unnecessary 
The package uses `argcomplete` to autocomplete arguments. Install it on your system using:

```
# on Ubuntu
sudo apt install python3-argcomplete
sudo activate-global-python-argcomplete
```
--->

#### Clone git repo

```
git clone https://github.com/gaheldev/godot-version-manager.git
cd godot-version-manager
```

#### Set up virtualenv (recommended)

We use virtualenv to create an environment with controlled python package versions. 


```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

Make sure to run `source venv/bin/activate` before working on the project. <br>
Run `deactivate` to deactivate the virtualenv.

#### Install godot-version-manager on your system

```
chmod +x install.sh
./install.sh
```

<br></br>



# 📝 Usage

### Update Godot

```
gvm download VERSION
gvm use VERSION
```

Both running ```godot``` in the terminal or opening Godot's desktop application will point to the new installed version.
<br> <br/>

### Use an already installed Godot version

Use as system's default
```
gvm use VERSION
```

Use as current working directory's version
```
gvm use --local VERSION
```

### Run Godot

`gvm run` runs the current working directory's version if it exists, otherwise runs system's default

### Advanced usage

Run ```gvm -h``` for more informations

<br></br>




# ⌨️ Development

### Tests

Tests are located in the `tests/` folder of the project. All test files should be named 'test_*.py' or '*_test.py'.

Run `pytest` in the project's root directory to run all tests. 

#### Automatically run tests before any commit

> [!WARNING]
> this will delete any pre-commit hook you already created
```
chmod +x pre-commit-hook.sh
./pre-commit-hook.sh
```

If you already have a pre-commit hook set up, just add the line `pytest` to `.git/hooks/pre-commit`
