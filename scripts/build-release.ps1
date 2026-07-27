param(
    [string]$Version = "1.0.0"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Dist = Join-Path $Root "dist"
$Stage = Join-Path $Dist "Cat-Cursor-macOS"
$Zip = Join-Path $Dist "Cat-Cursor-macOS-v$Version.zip"

if (Test-Path $Stage) { Remove-Item -Recurse -Force $Stage }
New-Item -ItemType Directory -Path (Join-Path $Stage "lib") -Force | Out-Null

Copy-Item (Join-Path $Root "mac\dist\Cat-Cursor.cape") (Join-Path $Stage "Cat-Cursor.cape") -ErrorAction Stop
Copy-Item (Join-Path $Root "mac\package\Install Cat Cursor.command") $Stage
Copy-Item (Join-Path $Root "mac\lib\install_core.sh") (Join-Path $Stage "lib\install_core.sh")
Copy-Item (Join-Path $Root "mac\package\README.txt") $Stage

New-Item -ItemType Directory -Path $Dist -Force | Out-Null
if (Test-Path $Zip) { Remove-Item -Force $Zip }
Compress-Archive -Path $Stage -DestinationPath $Zip

Write-Host "Created $Zip"
