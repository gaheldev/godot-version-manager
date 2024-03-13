#!powershell

Remove-Item .\build -Recurse -Force *> $null 
Remove-Item .\dist -Recurse -Force *> $null
Remove-Item .\*.completion -Force *> $null
Remove-Item .\*.spec -Force *> $null