#!powershell

echo "#!powershell

# run tests
pytest -v --online

# pass the failure code back to the pre-commit hook
exit $LASTEXITCODE
" > .git/hooks/pre-commit.ps1

echo "#!/bin/sh
echo 
exec pwsh.exe -ExecutionPolicy RemoteSigned -File '.\pre-commit.ps1'
exit
" > .git/hooks/pre-commit