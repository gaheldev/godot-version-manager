#!powershell

# Bin directory: where we create a wrapper script for gdvm to be in path
$BinDir = ($env:USERPROFILE + '\AppData\Local\bin\')
# Files directory: where we install gdvm files
$FilesDir = ($env:USERPROFILE + '\AppData\Local\Programs\godot-version-manager\libs\')
# Icon directory: where we copy the legacy godot icon for our godot versions installs
$LegacyIconDir = ($env:USERPROFILE + '\AppData\Local\Programs\Godot\')
# Cache directory: used for gdvm cache
$CacheDir = ($env:USERPROFILE + '\AppData\Local\Programs\godot-version-manager\cache\')

# Wrapper script path
$BinPath = ($BinDir + 'gdvm.ps1')
# Real gdvm binary path
$RealBin = ($FilesDir + 'gdvm.exe')
# Leagcy icon path
$LegacyIcon = ($LegacyIconDir + 'godot.png')

# Parse arguments
if ($args[0] -eq '--force') {
	$Force = $true
}

# Create directories if they're not already existing
New-Item -Path $BinDir -ItemType Directory -Force | Out-Null
New-Item -Path $FilesDir -ItemType Directory -Force | Out-Null
New-Item -Path $LegacyIconDir -ItemType Directory -Force | Out-Null

# Add BinDir to user's PATH if it's not already there
$CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if (-not (($CurrentPath -split [IO.Path]::PathSeparator).TrimEnd('\') -contains $BinDir.TrimEnd('\'))) {
	$NewPath = $CurrentPath.TrimEnd([IO.Path]::PathSeparator) + [IO.Path]::PathSeparator + $BinDir
	[Environment]::SetEnvironmentVariable( "PATH", $NewPath, "User" )
}

if (-not $Force) {
    # Remove previous LegacyIcon if it exists
	if (Test-Path $LegacyIcon) {
		Write-Output ('Deleting ' + $LegacyIcon + ' from a previous installation')
		Remove-Item -Path $LegacyIcon -Force | Out-Null
	}
}

Write-Output 'Installing gdvm'

# When autoupgrading, gdvm might still be busy
# Let's wait for gdvm to be done
Wait-Process -Name gdvm -Timeout 300 2> $null

# Remove previous wrapper script if it exists
if (Test-Path $BinPath) {
	Remove-Item -Path $BinPath -Force | Out-Null
}

# Copying gdvm files to installation directory
Copy-Item -Path 'dist\gdvm\*' -Destination $FilesDir -Recurse -Force | Out-Null

# Create powershell wrapper script
('#!powershell
Start-Process -FilePath ' + $RealBin + ' -ArgumentList $args -NoNewWindow'
) > $BinPath

# Copying the godot legacy icon
Copy-Item -Path '.\godot.png' -Destination $LegacyIcon -Recurse -Force | Out-Null

# Removing old cache  directory
((Remove-Item $CacheDir -Recurse -Force) -or $true) | Out-Null

Write-Output ('Installed gdvm to ' + $BinDir)

# Getting available Godot releases
gdvm sync
Wait-Process -Name gdvm -Timeout 300 2> $null

Write-Output '
=============================
Press ENTER to quit installer
'

# Wait for user ENTER input
Read-Host | Out-Null