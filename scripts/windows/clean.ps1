#!powershell

Remove-Item .\build -Recurse -Force
Remove-Item .\dist -Recurse -Force
Remove-Item .\*.completion
Remove-Item .\*.spec