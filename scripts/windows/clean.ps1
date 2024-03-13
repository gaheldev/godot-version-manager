#!pwsh

Remove-Item -Path .\build -Recurse -Force *> $null 
Remove-Item -Path .\dist -Recurse -Force *> $null
Remove-Item -Path .\*.completion -Force *> $null
Remove-Item -Path .\*.spec -Force *> $null