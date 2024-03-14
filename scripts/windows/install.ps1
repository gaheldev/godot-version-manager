#!pwsh

# Bin directory: where we create a wrapper script for gdvm to be in path
$BinDir = Join-Path $env:USERPROFILE \AppData\Local\bin\
# Files directory: where we install gdvm files
$FilesDir = Join-Path $env:USERPROFILE \AppData\Local\Programs\godot-version-manager\libs\
# Cache directory: used for gdvm cache
$CacheDir = Join-Path $env:USERPROFILE \AppData\Local\Programs\godot-version-manager\cache\

# Wrapper script path
$BinPath = Join-Path $BinDir gdvm.ps1
# Real gdvm binary path
$RealBin = Join-Path $FilesDir gdvm.exe

# Parse arguments
if ($args[0] -eq '--force') {
	# Kept for compatibility with linux implementation
	$Force = $true
}

# Create directories if they're not already existing
New-Item -Path $BinDir -ItemType Directory -Force | Out-Null
New-Item -Path $FilesDir -ItemType Directory -Force | Out-Null

# Add BinDir to user's PATH if it's not already there
$CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if (-not (($CurrentPath -split [IO.Path]::PathSeparator).TrimEnd('\') -contains $BinDir.TrimEnd('\'))) {
	$NewPath = @(
			$CurrentPath.TrimEnd([IO.Path]::PathSeparator)
			$BinDir
		) -join [IO.Path]::PathSeparator
	[Environment]::SetEnvironmentVariable("PATH", $NewPath, "User" ) | Out-Null
}

Write-Output 'Installing gdvm'

# When autoupgrading, gdvm might still be busy
# Let's wait for gdvm to be done
Wait-Process -Name gdvm -Timeout 300 2> $null

# Remove previous wrapper script if it exists
if (Test-Path $BinPath) {
	Remove-Item -Path $BinPath -Force *> $null
}

# Copying gdvm files to installation directory
Copy-Item -Path .\dist\gdvm\* -Destination $FilesDir -Recurse -Force | Out-Null

# Create powershell wrapper script
"#!pwsh
Start-Process -FilePath $RealBin -ArgumentList `$args -NoNewWindow
" > $BinPath

# Removing old cache  directory
Remove-Item -Path $CacheDir -Recurse -Force *> $null

Write-Output "Installed gdvm to $BinDir"

# Getting available Godot releases
gdvm sync
Wait-Process -Name gdvm -Timeout 300 2> $null

# TODO WIN: Test 'gdmv upgrade' command when a version is available
Write-Output '
=============================
Press ENTER to quit installer
'

# Wait for user ENTER input
Read-Host | Out-Null