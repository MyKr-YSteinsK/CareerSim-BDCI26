@echo off
setlocal
set "PYTHONPATH="
set "VIRTUAL_ENV="
set "PYTHONDONTWRITEBYTECODE=1"
set "MSGPACK_PUREPYTHON="
rem Resolve from the fixed persistent worktree; no system Python fallback.
set "HPL_WEB_PYTHON=%~dp0..\..\..\runtime\human-play-lab\local-web-client\venv\Scripts\python.exe"
if not exist "%HPL_WEB_PYTHON%" (
  echo HPL-05 runtime missing. Build the dedicated runtime before launching.
  pause
  exit /b 1
)
"%HPL_WEB_PYTHON%" -B "%~dp0hpl_web.py" %*
if errorlevel 1 pause
endlocal
