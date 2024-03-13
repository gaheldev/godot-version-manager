#!pwsh

Write-Output 'Creating release for linux...'

$System = 'windows'
$ReleaseDir = Join-Path .\release $System gdvm

New-Item -Path $ReleaseDir\dist -ItemType Directory -Force | Out-Null

Remove-Item -Path $ReleaseDir\dist\gdvm -Recurse -Force *> $null
Copy-Item -Path .\dist\gdvm -Destination $ReleaseDir\dist -Recurse | Out-Null
Copy-Item -Path .\gdvm.completion -Destination $ReleaseDir | Out-Null
Copy-Item -Path .\godot.png -Destination $ReleaseDir | Out-Null
Copy-Item -Path .\scripts\unix\install -Destination $ReleaseDir | Out-Null
Copy-Item -Path .\LICENSE -Destination $ReleaseDir | Out-Null


# TODO WIN: simplify
Set-Location -Path $ReleaseDir\..
$Archive = "gdvm_$System.zip"
zip -r $Archive gdvm
Wait-Process -Name zip -Timeout 300 2> $null
Move-Item -Path $Archive -Destination .. -Force | Out-Null

Write-Output "$System release created at release/$Archive"
