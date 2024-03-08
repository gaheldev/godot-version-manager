#!powershell


# TODO: add ~/.local/bin to path if it's not in it
$BinDir = ($env:USERPROFILE + '/.local/bin/')
$BinPath = ($BinDir + 'gdvm')
New-Item -Path $BinDir -ItemType Directory -Force

$FilesDir = ($env:USERPROFILE + '/.local/share/gdvm/libs/')
$RealBin = ($FilesDir + 'gdvm')
New-Item -Path $FilesDir -ItemType Directory -Force



if ($args[0] -eq '--force') {
	$Force = $true
}


$LegacyCompletion = '/usr/share/bash-completion/completions/gdvm'
$LegacyIcon = '/usr/share/share/pixmaps/godot.png'

if (-not $Force) {
	if (Test-Path $LegacyCompletion) {
		Write-Output ('Deleting ' + $LegacyCompletion + ' from a previous installation')
		Remove-Item -Path $LegacyCompletion -Force
	}

	if (Test-Path $LegacyIcon ) {
		Write-Output ('Deleting ' + $LegacyIcon + ' from a previous installation')
		Remove-Item -Path $LegacyIcon -Force
	}
}




# When autoupgrading, gdvm bin might still be busy, let's wait for gdvm to be done
Start-Sleep -Seconds 0.5
Write-Output 'Installing gdvm'
while (lsof $BinPath | Out-Null) {
	Write-Host -NoNewline '.'
	Start-Sleep -Seconds 0.5
}
Write-Host -NoNewline [Environment]::NewLine

# remove previous BIN if it exists
if (Test-Path $BinPath) {
	Remove-Item -Path $BinPath -Force
}

Copy-Item -Path dist/gdvm/* -Destination $FilesDir -Recurse
ln -s $RealBin $BinPath

mkdir -p ~/.local/share/bash-completion/completions
Copy-Item -Path gdvm.completion -Destination ~/.local/share/bash-completion/completions/gdvm

Copy-Item -Path godot.png -Destination ~/.local/share/icons/
rm -r ~/.cache/gdvm 2> /dev/null || true

Write-Output ('Installed gdvm to' + $BinDir)

gdvm sync


Write-Output '
=======================================================
Press ENTER to quit installer (ignore following errors)
'
