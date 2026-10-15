param([string]$Version = "candidate")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
# Builds a macOS package on Windows, NOT a Windows cursor installer.
# Python's ZIP writer retains executable bits, unlike Compress-Archive.
python (Join-Path $Root "scripts/build_release.py") --version $Version
if ($LASTEXITCODE -ne 0) { throw "Package build failed with exit code $LASTEXITCODE" }
