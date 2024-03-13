#!powershell

Write-Output 'Creating release for linux...'

$System = 'windows'
$Dir = ".\release\$System\gdvm"
New-Item -Path "$Dir\dist" -ItemType Directory -Force | Out-Null


((Remove-Item "$Dir\dist\gdvm" -Recurse -Force) -or $true) | Out-Null
Copy-Item -Path .\dist\gdvm -Destination "$Dir\dist" -Recurse | Out-Null
Copy-Item -Path .\gdvm.completion -Destination $Dir | Out-Null
Copy-Item -Path .\godot.png -Destination $Dir | Out-Null
Copy-Item -Path .\scripts\unix\install -Destination $Dir | Out-Null
Copy-Item -Path .\LICENSE -Destination $Dir | Out-Null


# TODO: simplify
Set-Location -Path "$Dir\.."
$Archive = "gdvm_$System.zip"
zip -r $Archive gdvm
Wait-Process -Name zip -Timeout 300 2> $null
Move-Item -Path $Archive -Destination .. -Force | Out-Null

Write-Output "$System release created at release/$Archive"
