@echo off
REM qobuz-dl with handy options for DJs
echo qbdl is a handy downloader using qobuz-dl with common options for DJs

set "mode=%1"
set "params=%*"
REM Remove the first argument (mode)
for /f "tokens=1,* delims= " %%a in ("%*") do set "params=%%b"

if "%mode%"=="dl" (
    echo [INFO] DJ Mode enabled: MP3 320kbps, Smart Discography, No DB, No Fallback, Embedded Art
) else (
    echo [ERROR] Invalid mode. Use 'dl' for DJ Mode.
    exit /b 1
)

set "cmd_flags=dl -D"

where uv >nul 2>nul
if %errorlevel% equ 0 (
    echo [INFO] Using uv...
    uv run python -m qobuz_dl %cmd_flags% %params%
    exit /b %errorlevel%
)

echo [INFO] uv not found. Trying mamba...
call mamba activate qobuz 2>nul
if %errorlevel% equ 0 (
    where uv >nul 2>nul
    if %errorlevel% equ 0 (
        echo [INFO] Using uv inside mamba...
        uv run python -m qobuz_dl %cmd_flags% %params%
    ) else (
        echo [INFO] Using qobuz-dl directly inside mamba...
        python -m qobuz_dl %cmd_flags% %params%
    )
    exit /b %errorlevel%
)

echo [INFO] mamba not found or failed. Trying qobuz-dl directly...
python -m qobuz_dl %cmd_flags% %params%