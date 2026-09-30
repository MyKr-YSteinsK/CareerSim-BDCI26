# HPL-04 Windows portable build

The release builder is `scripts/build-hpl-portable.ps1`. It uses the HPL-04A
accepted python.org CPython 3.12.10 environment at
`.local/runtime/human-play-lab/packaging-python/venv`, Flet 1.0.1 and PyInstaller
6.16.0. The build checks the base `python312.dll` Authenticode signature and
requires the bundled DLL to match its SHA256, Valid status and Python Software
Foundation signer.

The complete 194-file Dev dataset comes from the installed
`career_emulator_bdci26/dev/dataset` and is bound to its distribution RECORD.
The same bytes are packaged at the official `career_emulator/data/dataset`
default root, including `performance_score/config.data`, as well as the seven
explicit GameEngine dataset paths.

Packaged writable state lives beside the executable in `UserData/Runs`,
`UserData/Exports` and `UserData/Diagnostics`. Startup probes the application
directory and all three folders before exposing Start. If they are unwritable,
the app stops and asks the user to extract the complete folder to Desktop, D: or
another ordinary writable location; it does not switch storage roots.

Generated payload, signature inventory and release ZIP stay under the ignored
`.local/runtime/human-play-lab/package-build/` directory. The repository does
not track the executable, Python runtime, copied dataset, user data or ZIP.
The verifier checks the archive, bundled native signatures and source-path
markers, then performs isolated start-screen and in-memory fixture smoke tests
with no Python, Flet, uv or repository path available. A temporary denied-write
ACL checks fail-closed startup without creating a game.

The release state is
`HPL04_PORTABLE_ARTIFACT_READY_FOR_CLEAN_MACHINE_VALIDATION`. A user-controlled
run on an independent Windows 10/11 x64 machine remains pending. The generated
CareerSim Human executable is unsigned; trusted code signing is recommended for
broad external distribution. Do not disable Windows security or add exclusions.
