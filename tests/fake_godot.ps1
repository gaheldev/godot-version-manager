#!/usr/bin/env pwsh

$FakeVersion = '3.42.7.stable.official.666aa6aa'

switch ($args[0])
{
	{ $_ -in '-v', '--version'}  {
		Write-Output $FakeVersion
	}
	default {
	}
}
