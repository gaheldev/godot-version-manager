#!pwsh

# Creating powershell pre-commit hookscript
"#!pwsh

# run tests
pytest -v --online

# pass the failure code back to the pre-commit hook
exit `$LASTEXITCODE
" > .git\hooks\pre-commit.ps1

# Creating shell wrapper
$Wrapper = @"
#!/usr/bin/env sh
pwsh -File .git/hooks/pre-commit.ps1

"@
$Wrapper -replace "`r`n", "`n" | Out-File ".git/hooks/pre-commit" -Encoding utf8NoBOM -NoNewline
