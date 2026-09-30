param(
    [Parameter(Mandatory = $true, Position = 0)] [string]$Artifact,
    [switch]$SkipSmoke
)

$ErrorActionPreference = 'Stop'
$worktree = Split-Path $PSScriptRoot -Parent
$workspace = Split-Path (Split-Path (Split-Path $worktree -Parent) -Parent) -Parent
$runtime = Join-Path $workspace '.local\runtime\human-play-lab'
$packagingRoot = Join-Path $runtime 'packaging-python'
$packagingPython = Join-Path $packagingRoot 'venv\Scripts\python.exe'
$basePythonDll = Join-Path $packagingRoot 'cpython-3.12.10\python312.dll'
if (-not (Test-Path -LiteralPath $packagingPython -PathType Leaf)) { throw "Official CPython verifier is missing: $packagingPython" }
$resolvedArtifact = [IO.Path]::GetFullPath($Artifact)
if (-not (Test-Path -LiteralPath $resolvedArtifact -PathType Leaf)) { throw "Portable artifact is missing: $resolvedArtifact" }
$verifier = Join-Path $worktree 'packaging\windows\package_manifest.py'
$staticOutput = @(& $packagingPython $verifier verify $resolvedArtifact)
if ($LASTEXITCODE -ne 0) { throw "Portable static verification failed with exit code $LASTEXITCODE" }
$static = ($staticOutput -join "`n") | ConvertFrom-Json

$validationRoot = Join-Path ([IO.Path]::GetTempPath()) ('CareerSimHuman-Validation-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $validationRoot -Force | Out-Null
$readonlyRule = $null
$readonlyDirectory = $null
try {
    Expand-Archive -LiteralPath $resolvedArtifact -DestinationPath $validationRoot -Force
    $appRoot = Join-Path $validationRoot 'CareerSim-Human-v1'
    $exe = Join-Path $appRoot 'CareerSim Human.exe'
    if (-not (Test-Path -LiteralPath $exe -PathType Leaf)) { throw "Extracted portable executable is missing: $exe" }

    function Get-NativeRows([string]$Root, [string]$Prefix = '') {
        $rows = @()
        foreach ($file in Get-ChildItem -LiteralPath $Root -Recurse -File | Where-Object { $_.Extension.ToLowerInvariant() -in @('.exe', '.dll', '.pyd') }) {
            $relative = $file.FullName.Substring($Root.Length).TrimStart('\').Replace('\', '/')
            $signature = Get-AuthenticodeSignature -LiteralPath $file.FullName
            $subject = if ($signature.SignerCertificate) { $signature.SignerCertificate.Subject } else { '' }
            $classification = if ($signature.Status -eq 'NotSigned') {
                'UNSIGNED'
            } elseif ($signature.Status -ne 'Valid') {
                'INVALID_SIGNATURE'
            } elseif ($subject -match 'Python Software Foundation') {
                'PYTHON_SOFTWARE_FOUNDATION_SIGNED'
            } elseif ($subject -match 'Microsoft') {
                'MICROSOFT_SIGNED_BUNDLED'
            } else {
                'AUTHENTICODE_VALID_OTHER'
            }
            $rows += [PSCustomObject]@{
                path = ($Prefix + $relative)
                extension = $file.Extension.ToLowerInvariant()
                bytes = $file.Length
                sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
                authenticode_status = [string]$signature.Status
                signer_subject = $subject
                classification = $classification
                origin = if ($relative -eq 'CareerSim Human.exe') { 'PROJECT_GENERATED' } else { 'BUNDLED_RUNTIME_OR_DEPENDENCY' }
            }
        }
        return $rows
    }

    $native = @(Get-NativeRows $appRoot)
    $fletArchive = Join-Path $appRoot '_internal\flet_desktop\app\flet-windows.zip'
    if (-not (Test-Path -LiteralPath $fletArchive -PathType Leaf)) { throw 'Bundled Flet runtime archive is missing after extraction.' }
    $fletRoot = Join-Path $validationRoot 'flet-runtime-inventory'
    New-Item -ItemType Directory -Path $fletRoot -Force | Out-Null
    Expand-Archive -LiteralPath $fletArchive -DestinationPath $fletRoot -Force
    $native += @(Get-NativeRows $fletRoot '_internal/flet_desktop/app/flet-windows.zip!')

    $pythonDll = Join-Path $appRoot '_internal\python312.dll'
    if (-not (Test-Path -LiteralPath $pythonDll -PathType Leaf)) { throw 'Bundled _internal\python312.dll is missing.' }
    $pythonSignature = Get-AuthenticodeSignature -LiteralPath $pythonDll
    $pythonSigner = if ($pythonSignature.SignerCertificate) { $pythonSignature.SignerCertificate.Subject } else { '' }
    $pythonDllHash = (Get-FileHash -LiteralPath $pythonDll -Algorithm SHA256).Hash.ToLowerInvariant()
    $baseDllHash = (Get-FileHash -LiteralPath $basePythonDll -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($pythonSignature.Status -ne 'Valid' -or $pythonSigner -notmatch 'Python Software Foundation' -or $pythonDllHash -ne $baseDllHash) {
        throw "Bundled python312.dll signature or identity failed: status=$($pythonSignature.Status), signer='$pythonSigner', sha256=$pythonDllHash"
    }
    $mainSignature = Get-AuthenticodeSignature -LiteralPath $exe
    if ($mainSignature.Status -ne 'NotSigned') {
        throw "Generated CareerSim Human.exe was expected to be unsigned; found $($mainSignature.Status)."
    }

    $byClass = @{}
    foreach ($group in ($native | Group-Object classification)) { $byClass[$group.Name] = $group.Count }
    $byOrigin = @{}
    foreach ($group in ($native | Group-Object origin)) { $byOrigin[$group.Name] = $group.Count }
    $byStatus = @{}
    foreach ($group in ($native | Group-Object authenticode_status)) { $byStatus[$group.Name] = $group.Count }
    $invalidSignatureCount = @($native | Where-Object authenticode_status -eq 'Invalid').Count
    $nativeInventory = [ordered]@{
        schema = 'hpl-native-signature-inventory/v1'
        artifact_sha256 = $static.sha256
        native_file_count = $native.Count
        system_managed_file_count = 0
        invalid_signature_file_count = $invalidSignatureCount
        extension_counts = [ordered]@{
            exe = @($native | Where-Object extension -eq '.exe').Count
            dll = @($native | Where-Object extension -eq '.dll').Count
            pyd = @($native | Where-Object extension -eq '.pyd').Count
        }
        classification_counts = $byClass
        origin_counts = $byOrigin
        authenticode_status_counts = $byStatus
        python312 = [ordered]@{ path = '_internal/python312.dll'; sha256 = $pythonDllHash; authenticode_status = [string]$pythonSignature.Status; signer_subject = $pythonSigner }
        generated_exe = [ordered]@{ path = 'CareerSim Human.exe'; authenticode_status = [string]$mainSignature.Status; signer_subject = '' }
        files = $native
    }
    $inventoryPath = Join-Path (Split-Path $resolvedArtifact -Parent) 'native-signature-inventory.json'
    $nativeInventory | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $inventoryPath -Encoding utf8

    $userData = Join-Path $appRoot 'UserData'
    if (Test-Path -LiteralPath $userData) { throw 'Release bundle unexpectedly contains UserData or existing Human runs.' }
    $smokeResults = @()
    if (-not $SkipSmoke) {
        $profile = Join-Path $validationRoot 'isolated-profile'
        $localAppData = Join-Path $validationRoot 'isolated-local-appdata'
        $temp = Join-Path $validationRoot 'isolated-temp'
        New-Item -ItemType Directory -Path $profile, $localAppData, $temp -Force | Out-Null

        function Invoke-FixtureSmoke([string]$Screen, [string]$ReportPath) {
            $psi = [Diagnostics.ProcessStartInfo]::new()
            $psi.FileName = $exe
            $psi.WorkingDirectory = $appRoot
            $psi.UseShellExecute = $false
            $psi.CreateNoWindow = $true
            $psi.Environment.Clear()
            $psi.Environment['SystemRoot'] = $env:SystemRoot
            $psi.Environment['WINDIR'] = $env:SystemRoot
            $psi.Environment['PATH'] = (Join-Path $env:SystemRoot 'System32') + ';' + $env:SystemRoot
            $psi.Environment['USERPROFILE'] = $profile
            $psi.Environment['LOCALAPPDATA'] = $localAppData
            $psi.Environment['APPDATA'] = $localAppData
            $psi.Environment['TEMP'] = $temp
            $psi.Environment['TMP'] = $temp
            foreach ($arg in @('--fixture', '--fixture-screen', $Screen, '--smoke-seconds', '3', '--smoke-report', $ReportPath)) {
                $psi.ArgumentList.Add($arg)
            }
            foreach ($name in @('PYTHONPATH', 'VIRTUAL_ENV', 'FLET_VIEW_PATH', 'FLET_FORCE_WEB_SERVER', 'FLET_DISPLAY_URL_PREFIX', 'FLET_SERVER_IP', 'FLET_SERVER_PORT')) {
                if ($psi.Environment.ContainsKey($name)) { throw "Smoke environment unexpectedly contains $name." }
            }
            if ($psi.Environment['PATH'] -match 'python|uv|human-play-lab|CareerSim') {
                throw 'Smoke PATH includes Python, uv, the HPL runtime or the repository.'
            }
            try {
                $process = [Diagnostics.Process]::Start($psi)
            }
            catch {
                $startError = $_.Exception.GetBaseException().Message
                if ($startError -match '应用程序控制策略已阻止|application control policy has blocked|signing level|Code Integrity|AppLocker') {
                    throw "Windows Application Control blocked the unsigned packaged launcher during the $Screen fixture smoke. No security setting was changed. Run this gate in a policy-compatible Windows environment or obtain approved signing; raw error: $startError"
                }
                throw
            }
            if (-not $process.WaitForExit(45000)) {
                $process.Kill($true)
                throw "Portable $Screen fixture smoke exceeded the 45 second bound."
            }
            if ($process.ExitCode -ne 0) { throw "Portable $Screen fixture smoke exited $($process.ExitCode)." }
            if (-not (Test-Path -LiteralPath $ReportPath -PathType Leaf)) { throw "Portable $Screen smoke report is missing." }
            $report = Get-Content -LiteralPath $ReportPath -Raw | ConvertFrom-Json
            if (-not $report.fixture -or -not $report.page_session_connected -or $report.real_engine_imported) {
                throw "Portable $Screen smoke did not prove the fixture-only no-game boundary."
            }
            return $report
        }

        foreach ($screen in @('start', 'active')) {
            $report = Invoke-FixtureSmoke $screen (Join-Path $validationRoot "$screen-smoke.json")
            $smokeResults += [ordered]@{ screen = $screen; result = 'PASS'; phase = $report.phase; real_engine_imported = $report.real_engine_imported }
        }
        foreach ($directory in @('Runs', 'Exports', 'Diagnostics')) {
            if (-not (Test-Path -LiteralPath (Join-Path $userData $directory) -PathType Container)) {
                throw "Packaged writable UserData directory is missing: $directory"
            }
        }
        if ((Get-ChildItem -LiteralPath (Join-Path $userData 'Runs') -Force).Count -ne 0) { throw 'Fixture smoke created a run.' }
        if ((Get-ChildItem -LiteralPath (Join-Path $userData 'Exports') -Force).Count -ne 0) { throw 'Fixture smoke created an export.' }
        if (Test-Path -LiteralPath (Join-Path $localAppData 'CareerSimHuman')) { throw 'Packaged app wrote user data under LocalAppData.' }
        if (-not (Get-ChildItem -LiteralPath (Join-Path $userData 'Diagnostics' 'flet-client') -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1)) {
            throw 'Flet runtime was not provisioned from the bundled archive into portable UserData.'
        }

        # Apply a temporary deny-write ACL to a second extracted copy. The process can still read and run,
        # but cannot create a UserData probe beside the executable. It must stop before launching Flet or a game.
        $readonlyDirectory = Join-Path $validationRoot 'readonly-app'
        Copy-Item -LiteralPath $appRoot -Destination $readonlyDirectory -Recurse
        $sid = [Security.Principal.WindowsIdentity]::GetCurrent().User
        $rights = [Security.AccessControl.FileSystemRights]::CreateFiles -bor
            [Security.AccessControl.FileSystemRights]::CreateDirectories -bor
            [Security.AccessControl.FileSystemRights]::WriteData -bor
            [Security.AccessControl.FileSystemRights]::AppendData -bor
            [Security.AccessControl.FileSystemRights]::Delete -bor
            [Security.AccessControl.FileSystemRights]::DeleteSubdirectoriesAndFiles
        $inheritance = [Security.AccessControl.InheritanceFlags]::ContainerInherit -bor [Security.AccessControl.InheritanceFlags]::ObjectInherit
        $readonlyRule = [Security.AccessControl.FileSystemAccessRule]::new($sid, $rights, $inheritance, [Security.AccessControl.PropagationFlags]::None, [Security.AccessControl.AccessControlType]::Deny)
        $acl = Get-Acl -LiteralPath $readonlyDirectory
        $acl.AddAccessRule($readonlyRule)
        Set-Acl -LiteralPath $readonlyDirectory -AclObject $acl
        $readonlyExe = Join-Path $readonlyDirectory 'CareerSim Human.exe'
        $readonlyReport = Join-Path $validationRoot 'readonly-smoke.json'
        $psi = [Diagnostics.ProcessStartInfo]::new()
        $psi.FileName = $readonlyExe
        $psi.WorkingDirectory = $readonlyDirectory
        $psi.UseShellExecute = $false
        $psi.CreateNoWindow = $true
        $psi.Environment.Clear()
        $psi.Environment['SystemRoot'] = $env:SystemRoot
        $psi.Environment['WINDIR'] = $env:SystemRoot
        $psi.Environment['PATH'] = (Join-Path $env:SystemRoot 'System32') + ';' + $env:SystemRoot
        $psi.Environment['USERPROFILE'] = $profile
        $psi.Environment['LOCALAPPDATA'] = $localAppData
        $psi.Environment['APPDATA'] = $localAppData
        $psi.Environment['TEMP'] = $temp
        $psi.Environment['TMP'] = $temp
        foreach ($arg in @('--fixture', '--fixture-screen', 'start', '--smoke-report', $readonlyReport)) { $psi.ArgumentList.Add($arg) }
        try {
            $process = [Diagnostics.Process]::Start($psi)
        }
        catch {
            $startError = $_.Exception.GetBaseException().Message
            if ($startError -match '应用程序控制策略已阻止|application control policy has blocked|signing level|Code Integrity|AppLocker') {
                throw "Windows Application Control blocked the unsigned packaged launcher during the unwritable-directory fixture smoke. No security setting was changed. Raw error: $startError"
            }
            throw
        }
        if (-not $process.WaitForExit(20000)) { $process.Kill($true); throw 'Unwritable application-directory smoke timed out.' }
        if ($process.ExitCode -ne 0) { throw "Unwritable application-directory smoke exited $($process.ExitCode)." }
        $readonlyResult = Get-Content -LiteralPath $readonlyReport -Raw | ConvertFrom-Json
        if ($readonlyResult.startup_gate -ne 'FAIL_CLOSED' -or $readonlyResult.page_session_connected -or $readonlyResult.real_engine_imported -or $readonlyResult.startup_error -notmatch '应用目录') {
            throw 'Unwritable application-directory smoke did not fail closed before Flet/game startup.'
        }
        if (Test-Path -LiteralPath (Join-Path $localAppData 'CareerSimHuman')) { throw 'Unwritable smoke silently fell back to LocalAppData.' }
        $smokeResults += [ordered]@{ screen = 'read_only_application_directory'; result = 'PASS'; game_started = $false; fallback = $false }
        $acl = Get-Acl -LiteralPath $readonlyDirectory
        $acl.RemoveAccessRuleAll($readonlyRule)
        Set-Acl -LiteralPath $readonlyDirectory -AclObject $acl
    }

    $validation = [ordered]@{
        schema = 'hpl-portable-validation/v1'
        artifact = [ordered]@{ path = [IO.Path]::GetFileName($resolvedArtifact); bytes = (Get-Item -LiteralPath $resolvedArtifact).Length; sha256 = $static.sha256 }
        static_package_verify = 'PASS'
        isolated_unpack = 'PASS'
        smoke_skipped = [bool]$SkipSmoke
        packaged_fixture_smoke = if ($SkipSmoke) { 'NOT_RUN' } else { 'PASS' }
        smoke_results = $smokeResults
        user_data = [ordered]@{ expected_root = 'CareerSim-Human-v1/UserData'; directories = @('Runs', 'Exports', 'Diagnostics'); writable_smoke = if ($SkipSmoke) { 'NOT_RUN' } else { 'PASS' }; unwritable_fail_closed_smoke = if ($SkipSmoke) { 'NOT_RUN' } else { 'PASS' } }
        native_inventory = [IO.Path]::GetFileName($inventoryPath)
        python312 = $nativeInventory.python312
        generated_exe = $nativeInventory.generated_exe
        source_path_leak_scan = 'PASS'
        local_python_flet_repo_dependency = if ($SkipSmoke) { 'NOT_RUN' } else { 'NOT_REQUIRED_IN_ISOLATED_SMOKE' }
    }
    $validation | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path (Split-Path $resolvedArtifact -Parent) 'PORTABLE_VALIDATION.json') -Encoding utf8
    Write-Output "NATIVE_FILES=$($native.Count)"
    Write-Output "NATIVE_CLASSIFICATIONS=$($byClass | ConvertTo-Json -Compress)"
    Write-Output "PYTHON312_SHA256=$pythonDllHash"
    Write-Output "PYTHON312_AUTHENTICODE=$($pythonSignature.Status)"
    Write-Output "PYTHON312_SIGNER=$pythonSigner"
    Write-Output "GENERATED_EXE_AUTHENTICODE=$($mainSignature.Status)"
    if ($SkipSmoke) { Write-Output 'ISOLATED_SMOKE=SKIPPED' } else { Write-Output 'ISOLATED_START_FIXTURE=PASS'; Write-Output 'ISOLATED_ACTIVE_FIXTURE=PASS'; Write-Output 'WRITABLE_USERDATA=PASS'; Write-Output 'READONLY_APP_DIR_FAIL_CLOSED=PASS' }
    Write-Output 'STATIC_PORTABLE_VERIFY=PASS'
}
finally {
    if ($readonlyRule -and $readonlyDirectory -and (Test-Path -LiteralPath $readonlyDirectory)) {
        try {
            $acl = Get-Acl -LiteralPath $readonlyDirectory
            $acl.RemoveAccessRuleAll($readonlyRule)
            Set-Acl -LiteralPath $readonlyDirectory -AclObject $acl
        } catch { }
    }
    if (Test-Path -LiteralPath $validationRoot) { Remove-Item -LiteralPath $validationRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
