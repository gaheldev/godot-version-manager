# Godot Version Manager

Use `gvm` from the command line to manage the Godot version of your different projects.

<br/>

> [!WARNING]
> currently under development, breaking changes will happen

<br/>


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

>[!IMPORTANT]
> `python > 3.11` is required. If necessary, install it from your package manager as well as `pip` for Python 3.

<!--- Seems unnecessary 
The package uses `argcomplete` to autocomplete arguments. Install it on your system using:

```
# on Ubuntu
sudo apt install python3-argcomplete
sudo activate-global-python-argcomplete
```
--->

## Clone git repo

```
git clone https://github.com/gaheldev/godot-version-manager.git
cd godot-version-manager
```

## Set up virtualenv (recommended)

We use virtualenv to create an environment with controlled python package versions. 


```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

Make sure to run `source venv/bin/activate` before working on the project. <br>
Run `deactivate` to deactivate the virtualenv.

## Install godot-version-manager on your system

```
chmod +x install.sh
./install.sh
```

<br></br>



# 📝 Usage

>[!NOTE]
> Run ```gvm -h``` for advanced usage

## Use Godot version in current working directory

```
gvm download VERSION_NUMBER --release RELEASE
gvm use --local VERSION
```

Gvm supports autocompletion of all arguments including all possible version and release names.  
Alternatively you can use the interactive version of the commands:
```
gvm download
gvm use --local
```


## Use an already managed version as system's default
```
gvm use --system VERSION
```
or for the interactive version:
```
gvm use --system
```

Both running ```godot``` in the terminal or opening Godot's desktop application will point to the new installed version.  
<br/>


## Run Godot

* `gvm run` runs the current working directory's project with project's version if it has been previously defined, otherwise asks to select the version to run.
  
* `gvm run VERSION` to run a specific version
  
* `gvm run --system` to run the system's default

<br><br/>




# ⌨️ Development

## Tests

Tests are located in the `tests/` folder of the project. All test files should be named 'test_*.py' or '*_test.py'.

Run `pytest` in the project's root directory to run all tests. 

### Automatically run tests before any commit

> [!WARNING]
> this will delete any pre-commit hook you already created
```
chmod +x pre-commit-hook.sh
./pre-commit-hook.sh
```

If you already have a pre-commit hook set up, just add the line `pytest` to `.git/hooks/pre-commit`
