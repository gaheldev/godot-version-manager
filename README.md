<h1 align='center'>
Godot Version Manager
</h1>

<p align='center'>
A command line tool to download and manage Godot versions per project
</p>

<br/>

<div align="center">
<a href=https://github.com/gaheldev/godot-version-manager/releases/latest alt="Latest release">
	<img src=https://img.shields.io/github/v/release/gaheldev/godot-version-manager>
</a>
</div>

<br/>


https://github.com/gaheldev/godot-version-manager/assets/78329601/886a3e13-cfba-417c-9473-98f12debcaa4






# ✨ Features

* download any release of Godot > 3.0 from the command line
* use a Godot version per project and track it with git
* set a system's default version of Godot, with desktop shortcut

<br/>

* [x] linux 🐧
* [ ] windows 🪟 (incoming)
* [ ] macos 🍎

<br></br>


---

# 🛠️ Installation

Download the [latest release](https://github.com/gaheldev/godot-version-manager/releases/latest) and extract it.  
Install `gdvm` by running the install script from the extracted directory:

```
cd gdvm
./install
```

>[!NOTE]
> If you encounter a glibc error follow the [install instructions for developers](#set-up-the-development-environment)

<br></br>

---

# 📝 Basic usage

Run ```gdvm -h``` for advanced usage

## Set a Godot version to use for current working directory
```
gdvm download VERSION_NUMBER
gdvm use VERSION
```
`gdvm` supports autocompletion of all arguments including all possible versions. 

Alternatively you can use the interactive mode:
```
gdvm download
gdvm use
```

If you'd like to use a release other than stable, such as `rc1` or `dev5`, you can use the `--release` argument:
```
gdvm download VERSION_NUMBER --release RELEASE
gdvm use VERSION
```

>[!NOTE]
> The local version is written to `.godotversion` in the current working directory. 
> Track it with git ;) 
<br/>

## Set a managed version as system's default
```
gdvm use --system-default VERSION
```
or for the interactive mode:
```
gdvm use --system-default
```

Both running ```godot``` in the terminal or opening Godot's desktop application will point to the new installed version.  
<br/>


## Run Godot

* `gdvm run` runs the current working directory's project with project's version if it has been previously defined, otherwise asks to select the version to run.
  
* `gdvm run VERSION` to run a specific version
  
* `gdvm run --system` to run the system's default

<br><br/>


---

# ⌨️ Development

## Set up the development environment

>[!IMPORTANT]
> `python > 3.11` is required. If necessary, install it from your package manager as well as `pip` for Python 3.
<br/>

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

#### Install gdvm on your system

```
make install
```

#### Git hooks

> [!WARNING]
> this will delete any pre-commit hook you already created

To automatically run tests before commits we use a pre-commit hook:

```
make hook
```

> [!WARNING]
> if a hook has been changed by you or someone else, you need to run `make hook` again

## Tests

Tests are located in the `tests/` folder of the project. All test files should be named 'test_\*.py' or '\*_test.py'.

Run `make tests` in the project's root directory to run all tests.


## Releases

Releases are automatically built on github when a tag `v*.*.*` is pushed by one of the commands:

```
make patch-release
make minor-release
make major-release
```
