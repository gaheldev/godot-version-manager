#!powershell

# TODO WIN : Add comments

# TODO WIN : Move this function to another file
function Test-File-Available {
    param (
          [string] $Path = $null
      )

    if (($Path -eq -$null) -or (-Not (Test-Path -Path $Path))) {
        # File does not exist
        return $false
    }

    try {
        $oFile = New-Object System.IO.FileInfo $Path
        $oStream = $oFile.Open(
            [System.IO.FileMode]::Open,
            [System.IO.FileAccess]::ReadWrite,
            [System.IO.FileShare]::None
        )

        if ($oStream) {
            $oStream.Close()
        }

        return $true
    } catch {
      # File is locked by a process.
      return $false
    }
}

$BinDir = ($env:USERPROFILE + '\AppData\Local\bin\')
$BinPath = ($BinDir + 'gdvm.ps1')
New-Item -Path $BinDir -ItemType Directory -Force | Out-Null

$CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if (-not (($CurrentPath -split [IO.Path]::PathSeparator).TrimEnd('\') -contains $BinDir.TrimEnd('\'))) {
	$NewPath = $CurrentPath.TrimEnd([IO.Path]::PathSeparator) + [IO.Path]::PathSeparator + $BinDir
	[Environment]::SetEnvironmentVariable( "PATH", $NewPath, "User" )
}

$FilesDir = ($env:USERPROFILE + '\AppData\Local\Programs\godot-version-manager\libs\')
$RealBin = ($FilesDir + 'gdvm.exe')
New-Item -Path $FilesDir -ItemType Directory -Force | Out-Null



if ($args[0] -eq '--force') {
	$Force = $true
}



$LegacyIconDir = ($env:USERPROFILE + '\AppData\Local\Programs\Godot\')
$LegacyIcon = ($LegacyIconDir + 'godot.png')

if (-not $Force) {
	if (Test-Path $LegacyIcon | Out-Null) {
		Write-Output ('Deleting ' + $LegacyIcon + ' from a previous installation')
		Remove-Item -Path $LegacyIcon -Force | Out-Null
	}
}


# When autoupgrading, gdvm bin might still be busy, let's wait for gdvm to be done
Start-Sleep -Seconds 0.5
Write-Output 'Installing gdvm'
while ((Test-File-Available $BinPath) | Out-Null) {
	Write-Host -NoNewline '.'
	Start-Sleep -Seconds 0.5
}
Write-Output ''

# Remove previous BIN if it exists
if (Test-Path $BinPath) {
	Remove-Item -Path $BinPath -Force | Out-Null
}

Copy-Item -Path 'dist\gdvm\*' -Destination $FilesDir -Recurse -Force | Out-Null
# Create powershell wrapper script
('#!powershell
Start-Process -FilePath ' + $RealBin + ' -ArgumentList $args -NoNewWindow'
) > $BinPath

$CacheDir = ($env:USERPROFILE + '\AppData\Local\Programs\godot-version-manager\cache\')

New-Item -Path $LegacyIconDir -ItemType Directory -Force | Out-Null
Copy-Item -Path '.\godot.png' -Destination $LegacyIcon -Recurse -Force | Out-Null
((Remove-Item $CacheDir -Recurse -Force) -or $true) | Out-Null

Write-Output ('Installed gdvm to ' + $BinDir)

gdvm sync
Wait-Process -Name pwsh -Timeout 300 2> $null

Write-Output '
=============================
Press ENTER to quit installer
'
Read-Host | Out-Null