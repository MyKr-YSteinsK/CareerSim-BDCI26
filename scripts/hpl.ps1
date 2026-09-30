[CmdletBinding()]
param(
    [switch]$Live,
    [string]$AuthorizationId,
    [string]$Tag = 'manual'
)

$ErrorActionPreference = 'Stop'
$worktreeRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$workspaceRoot = (Resolve-Path (Join-Path $worktreeRoot '..\..\..')).Path
$expectedWorktree = [IO.Path]::GetFullPath((Join-Path $workspaceRoot '.local\worktrees\human-play-lab'))
if ([IO.Path]::GetFullPath($worktreeRoot) -ne $expectedWorktree) {
    Write-Error "HPL launcher must run from the persistent worktree: $expectedWorktree"
    exit 2
}

$sandboxRoot = Join-Path $workspaceRoot '.local\runtime\human-play-lab'
$python = Join-Path $sandboxRoot 'venv\Scripts\python.exe'
$launcher = Join-Path $worktreeRoot 'scripts\hpl_play.py'
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    Write-Error "Dedicated HPL Python interpreter is missing: $python"
    exit 2
}

$arguments = @($launcher)
if ($Live) {
    $arguments += '--live'
}
if ($PSBoundParameters.ContainsKey('AuthorizationId')) {
    $arguments += @('--authorization-id', $AuthorizationId)
}
if ($PSBoundParameters.ContainsKey('Tag')) {
    $arguments += @('--tag', $Tag)
}

& $python @arguments
exit $LASTEXITCODE
