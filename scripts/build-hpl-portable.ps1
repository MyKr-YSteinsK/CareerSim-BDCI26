param(
    [switch]$SkipBuild,
    [switch]$SkipSmoke
)

$ErrorActionPreference = 'Stop'

$worktree = Split-Path $PSScriptRoot -Parent
$workspace = Split-Path (Split-Path (Split-Path $worktree -Parent) -Parent) -Parent
$expected = Join-Path $workspace '.local\worktrees\human-play-lab'
if ([IO.Path]::GetFullPath($worktree) -ne [IO.Path]::GetFullPath($expected)) {
    throw "Use the persistent HPL worktree: $expected"
}

$runtime = Join-Path $workspace '.local\runtime\human-play-lab'
$packagingRoot = Join-Path $runtime 'packaging-python'
$packageVenv = Join-Path $packagingRoot 'venv'
$packagingPython = Join-Path $packageVenv 'Scripts\python.exe'
$flet = Join-Path $packageVenv 'Scripts\flet.exe'
$sitePackages = Join-Path $packageVenv 'Lib\site-packages'
$datasetSource = Join-Path $sitePackages 'career_emulator_bdci26\dev\dataset'
$fletArchiveSource = Join-Path $runtime 'flet-runtime\1.0.1\flet-windows.zip'
$expectedFletArchiveHash = 'ef3b02b22f9d00ef35775930e33807f19380a0455999f452b058f00e104c4d09'
$entry = Join-Path $worktree 'hpl_client\app.py'
$dist = Join-Path $runtime 'package-build\dist'
$release = Join-Path $runtime 'package-build\release'
$packageBuild = Join-Path $runtime 'package-build'
$fletRuntimeSource = Join-Path $packageBuild 'flet-runtime-source'
$packCwd = Join-Path $packageBuild 'pack-cwd'
$payload = Join-Path $release 'CareerSim-Human-v1'
$zip = Join-Path $release 'CareerSim-Human-v1-Windows-x64.zip'
$basePythonDll = Join-Path $packagingRoot 'cpython-3.12.10\python312.dll'

foreach ($target in @($packagingPython, $flet, $entry, $basePythonDll, $datasetSource, $fletArchiveSource)) {
    if (-not (Test-Path -LiteralPath $target)) {
        throw "Required signed-CPython packaging input is missing: $target"
    }
}
$fletSourceHash = (Get-FileHash -LiteralPath $fletArchiveSource -Algorithm SHA256).Hash.ToLowerInvariant()
if ($fletSourceHash -ne $expectedFletArchiveHash) {
    throw "Previously verified Flet 1.0.1 Windows archive identity changed: $fletSourceHash"
}

if (-not $SkipBuild) {
    $dirty = @(& git -C $worktree status --porcelain --untracked-files=all)
    if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect the HPL source tree.' }
    if ($dirty.Count -gt 0) {
        throw 'Commit the exact HPL source before packaging so BUILD_MANIFEST.json identifies the packaged commit.'
    }
    $sourceCommit = (& git -C $worktree rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $sourceCommit) { throw 'Unable to identify the HPL source commit.' }

    $pythonIdentity = @(& $packagingPython -c "import platform,sys; print(platform.python_implementation()); print('.'.join(map(str,sys.version_info[:3])))")
    if ($LASTEXITCODE -ne 0 -or $pythonIdentity[0] -ne 'CPython' -or $pythonIdentity[1] -ne '3.12.10') {
        throw "Release packaging requires official CPython 3.12.10; found $($pythonIdentity -join ' ')"
    }
    $pythonRoots = @(& $packagingPython -c "import sys; print(sys.prefix); print(sys.base_prefix)")
    $expectedBase = Join-Path $packagingRoot 'cpython-3.12.10'
    if ([IO.Path]::GetFullPath($pythonRoots[0]) -ne [IO.Path]::GetFullPath($packageVenv) -or [IO.Path]::GetFullPath($pythonRoots[1]) -ne [IO.Path]::GetFullPath($expectedBase)) {
        throw "Packaging interpreter is not isolated on the accepted CPython base: $($pythonRoots -join ' | ')"
    }
    $signature = Get-AuthenticodeSignature -LiteralPath $basePythonDll
    $signer = if ($signature.SignerCertificate) { $signature.SignerCertificate.Subject } else { '' }
    if ($signature.Status -ne 'Valid' -or $signer -notmatch 'Python Software Foundation') {
        throw "Official packaging python312.dll signature gate failed: $($signature.Status), signer='$signer'"
    }
    $expectedPythonDllHash = (Get-FileHash -LiteralPath $basePythonDll -Algorithm SHA256).Hash.ToLowerInvariant()
    $metadata = @(& $packagingPython -c "import importlib.metadata as m; print('|'.join(m.version(n) for n in ('career-emulator','career-emulator-bdci26','flet','flet-desktop','pyinstaller')))" )
    if ($LASTEXITCODE -ne 0 -or $metadata[0] -ne '1.0.1|1.0.0|1.0.1|1.0.1|6.16.0') {
        throw "Packaging dependency identity is not frozen as requested: $($metadata -join ' ')"
    }

    if (Test-Path -LiteralPath $packageBuild) {
        $resolved = [IO.Path]::GetFullPath($packageBuild)
        $runtimePrefix = [IO.Path]::GetFullPath($runtime).TrimEnd('\') + '\'
        if (-not $resolved.StartsWith($runtimePrefix, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to clean a package path outside the HPL runtime: $resolved"
        }
        Remove-Item -LiteralPath $packageBuild -Recurse -Force
    }
    New-Item -ItemType Directory -Path $packCwd, $dist, $release -Force | Out-Null
    New-Item -ItemType Directory -Path $fletRuntimeSource -Force | Out-Null
    Expand-Archive -LiteralPath $fletArchiveSource -DestinationPath $fletRuntimeSource -Force
    if (-not (Test-Path -LiteralPath (Join-Path $fletRuntimeSource 'flet\flet.exe') -PathType Leaf)) {
        throw 'Pinned Flet archive does not contain its expected flet\flet.exe client.'
    }

    # Restrict all subprocess resolution to the official packaging venv and Windows.
    $env:VIRTUAL_ENV = $packageVenv
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
    $env:FLET_VIEW_PATH = $fletRuntimeSource
    foreach ($name in @('FLET_FORCE_WEB_SERVER', 'FLET_DISPLAY_URL_PREFIX', 'FLET_SERVER_IP', 'FLET_SERVER_PORT')) {
        Remove-Item "Env:$name" -ErrorAction SilentlyContinue
    }
    $env:PATH = (Join-Path $packageVenv 'Scripts') + ';' + (Join-Path $env:SystemRoot 'System32') + ';' + $env:SystemRoot

    $datasetArgument = $datasetSource + ';career_emulator/data/dataset'
    $packArgs = @(
        'pack', $entry, '--onedir', '--name', 'CareerSim Human', '--distpath', $dist,
        '--add-data', $datasetArgument,
        '--hidden-import', 'career_emulator.game',
        '--hidden-import', 'scripts.hpl_evidence_writer',
        '--hidden-import', 'scripts.hpl_public_evidence',
        '--pyinstaller-build-args=--exclude-module=gitcode_api',
        '--pyinstaller-build-args=--exclude-module=fastmcp',
        '--pyinstaller-build-args=--exclude-module=jiuwenswarm',
        '--pyinstaller-build-args=--exclude-module=career_emulator.cli',
        '--pyinstaller-build-args=--exclude-module=career_emulator.share_run',
        '--pyinstaller-build-args=--exclude-module=career_emulator.server',
        '--product-name', 'CareerSim Human', '--file-description', 'CareerSim Human portable client',
        '--product-version', '1.0.0', '--file-version', '1.0.0.0', '--yes'
    )
    Push-Location $packCwd
    try {
        & $flet @packArgs
        if ($LASTEXITCODE -ne 0) { throw "signed-CPython flet pack failed with exit code $LASTEXITCODE" }
    }
    finally { Pop-Location }

    $built = Join-Path $dist 'CareerSim Human'
    if (-not (Test-Path -LiteralPath (Join-Path $built 'CareerSim Human.exe') -PathType Leaf)) {
        throw "Flet onedir output is missing the expected executable: $built"
    }
    Move-Item -LiteralPath $built -Destination $payload
    $internal = Join-Path $payload '_internal'
    foreach ($pattern in @('gitcode_api', 'fastmcp', 'jiuwenswarm', 'career_emulator\cli.py', 'career_emulator\share_run.py', 'career_emulator\server')) {
        $candidate = Join-Path $internal $pattern
        if (Test-Path -LiteralPath $candidate) { Remove-Item -LiteralPath $candidate -Recurse -Force }
    }
    foreach ($pattern in @('gitcode_api-*.dist-info', 'fastmcp-*.dist-info', 'jiuwenswarm-*.dist-info')) {
        Get-ChildItem -LiteralPath $internal -Directory -Filter $pattern -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force
    }
    $packagedPythonDll = Join-Path $payload '_internal\python312.dll'
    if (-not (Test-Path -LiteralPath $packagedPythonDll -PathType Leaf)) {
        throw 'The onedir bundle is missing _internal\python312.dll.'
    }
    $actualPythonDllHash = (Get-FileHash -LiteralPath $packagedPythonDll -Algorithm SHA256).Hash.ToLowerInvariant()
    $packagedSignature = Get-AuthenticodeSignature -LiteralPath $packagedPythonDll
    $packagedSigner = if ($packagedSignature.SignerCertificate) { $packagedSignature.SignerCertificate.Subject } else { '' }
    if ($actualPythonDllHash -ne $expectedPythonDllHash -or $packagedSignature.Status -ne 'Valid' -or $packagedSigner -notmatch 'Python Software Foundation') {
        throw "Bundled _internal\python312.dll differs from the signed CPython runtime: SHA256=$actualPythonDllHash; signature=$($packagedSignature.Status); signer='$packagedSigner'"
    }
    $packagedFletArchive = Join-Path $payload '_internal\flet_desktop\app\flet-windows.zip'
    if (-not (Test-Path -LiteralPath $packagedFletArchive -PathType Leaf)) { throw 'The bundled Flet archive is missing.' }
    Copy-Item -LiteralPath $fletArchiveSource -Destination $packagedFletArchive -Force
    $packagedFletHash = (Get-FileHash -LiteralPath $packagedFletArchive -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($packagedFletHash -ne $expectedFletArchiveHash) { throw "Bundled Flet archive hash mismatch: $packagedFletHash" }

    & $packagingPython (Join-Path $worktree 'packaging\windows\package_manifest.py') create `
        '--bundle-root' $payload `
        '--dataset-source' $datasetSource `
        '--site-packages' $sitePackages `
        '--source-commit' $sourceCommit `
        '--build-command' ('flet pack --onedir --add-data <career_emulator_bdci26/dev/dataset>;career_emulator/data/dataset --pyinstaller-build-args=exclude-provider-modules;FLET_VIEW_PATH=<pinned-flet-runtime> sha256=' + $expectedFletArchiveHash)
    if ($LASTEXITCODE -ne 0) { throw "Portable BUILD_MANIFEST generation failed with exit code $LASTEXITCODE" }
    Compress-Archive -Path $payload -DestinationPath $zip -CompressionLevel Optimal
}

if (-not (Test-Path -LiteralPath $zip -PathType Leaf)) { throw "Portable ZIP is missing: $zip" }
$verify = Join-Path $worktree 'scripts\verify-hpl-portable.ps1'
& $verify $zip -SkipSmoke:$SkipSmoke
if ($LASTEXITCODE -ne 0) { throw "Portable artifact verification failed with exit code $LASTEXITCODE" }
$hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
$bytes = (Get-Item -LiteralPath $zip).Length
Set-Content -LiteralPath ($zip + '.sha256') -Value "$hash  $([IO.Path]::GetFileName($zip))" -Encoding ascii
$status = if ($SkipSmoke) { 'HPL04_STATIC_PORTABLE_BUILD_ONLY_SMOKE_PENDING' } else { 'HPL04_PORTABLE_ARTIFACT_READY_FOR_CLEAN_MACHINE_VALIDATION' }
$releaseSidecar = [ordered]@{
    artifact = [ordered]@{ path = [IO.Path]::GetFileName($zip); bytes = $bytes; sha256 = $hash }
    package_status = $status
    packaged_fixture_smoke = if ($SkipSmoke) { 'NOT_RUN' } else { 'PASS' }
    clean_machine_status = 'CLEAN_MACHINE_VALIDATION_PENDING_USER_SMOKE'
}
$releaseSidecar | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $release 'BUILD_MANIFEST.release.json') -Encoding utf8
Write-Output "ARTIFACT=$zip"
Write-Output "BYTES=$bytes"
Write-Output "SHA256=$hash"
Write-Output "STATUS=$status"
