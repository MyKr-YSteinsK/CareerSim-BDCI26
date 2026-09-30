# HPL-04 Windows portable build

The release builder is `scripts/build-hpl-portable.ps1`. It uses the HPL-04A
accepted python.org CPython 3.12.10 environment at
`.local/runtime/human-play-lab/packaging-python/venv`, Flet 1.0.1 and PyInstaller
6.16.0. The build checks the base `python312.dll` Authenticode signature and
requires the bundled DLL to match its SHA256, Valid status and Python Software
Foundation signer.

Flet's wheel does not contain the Windows desktop archive; the build reuses the
previously statically checked Flet 1.0.1 archive at
`.local/runtime/human-play-lab/flet-runtime/1.0.1/flet-windows.zip` and pins it
to SHA256 `ef3b02b22f9d00ef35775930e33807f19380a0455999f452b058f00e104c4d09`.
The builder extracts it into its ignored build directory and supplies that
folder through `FLET_VIEW_PATH`, then restores the pinned archive bytes into
the payload after `flet pack`. It does not use `%USERPROFILE%\.flet` or download
the desktop runtime.

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
markers, then attempts isolated start-screen and in-memory fixture smoke tests
with no Python, Flet, uv or repository path available. A temporary denied-write
ACL checks fail-closed startup without creating a game. `-SkipSmoke` produces
only `HPL04_STATIC_PORTABLE_BUILD_ONLY_SMOKE_PENDING`; it cannot mark the
artifact ready.

During the current HPL-04 validation, Windows Application Control rejected the
unsigned generated launcher before app code ran, citing the Enterprise signing
level policy. The verifier reports this as an environment blocker; it does not
change security settings or claim a packaged smoke pass. The generated
CareerSim Human executable remains unsigned; trusted code signing is
recommended for broad external distribution. Do not disable Windows security
or add exclusions. See [HPL-04 review](../../docs/project/reviews/HPL-04_WINDOWS_PORTABLE_PACKAGING.md)
for the exact artifact and validation boundary.
