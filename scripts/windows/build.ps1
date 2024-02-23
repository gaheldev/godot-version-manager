#!powershell

pip install -r requirements.txt

$Tag = git describe --tags
$Branch = git branch --show-current

Switch ($Branch)
{
	{ $_ -in 'main',''}  {
		$Version = $Tag
	}
	default {
		$Version = ($Tag + ':' + $Branch)
	}
}

echo ('# DO NOT EDIT: automatically generated during build

__version__ = "' + $Version + '"
') > gdvm/version.py


echo ('Building gdvm: version ' + $Version)
pyinstaller -D main.py -n gdvm

cd dist/gdvm/
register-python-argcomplete gdvm > ../../gdvm.completion
cd ../..
rm gdvm/version.py
