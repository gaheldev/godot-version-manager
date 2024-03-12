#!powershell

pip install -r requirements.txt
Wait-Process -Name pip -Timeout 600 2> $null

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
pyinstaller -D main.py -n gdvm --noconfirm
Wait-Process -Name pyinstaller -Timeout 600 2> $null

#cd dist/gdvm/
# TODO WIN : Register argcomplete for windows
#register-python-argcomplete gdvm > ../../gdvm.completion
#cd ../..
rm gdvm/version.py
