param([switch]$Fixture, [int]$SmokeSeconds = 0, [string]$SmokeReport = '')
$ErrorActionPreference = 'Stop'
$taskWorktree = Split-Path $PSScriptRoot -Parent
$taskWorkspace = Split-Path (Split-Path (Split-Path $taskWorktree -Parent) -Parent) -Parent
$expected = Join-Path $taskWorkspace '.local\worktrees\human-play-lab'
if ([IO.Path]::GetFullPath($taskWorktree) -ne [IO.Path]::GetFullPath($expected)) { throw 'Use the persistent HPL worktree.' }
if (($SmokeSeconds -or $SmokeReport) -and -not $Fixture) { throw 'Smoke options require Fixture.' }
$humanPython = Join-Path $taskWorkspace '.local\runtime\human-play-lab\venv\Scripts\python.exe'
$taskArgs = @('-m', 'hpl_client.app')
if ($Fixture) { $taskArgs += '--fixture' }
if ($SmokeSeconds) { $taskArgs += @('--smoke-seconds', "$SmokeSeconds") }
if ($SmokeReport) { $taskArgs += @('--smoke-report', $SmokeReport) }
Push-Location $taskWorktree
try { & $humanPython @taskArgs; if ($LASTEXITCODE -ne 0) { throw "HPL UI exit $LASTEXITCODE" } }
finally { Pop-Location }
