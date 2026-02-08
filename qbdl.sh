#!/bin/bash

MODE="$1"
shift

if [ "$MODE" == "dl" ]; then
    echo "[INFO] DJ Mode enabled: MP3 320kbps, Smart Discography, No DB, No Fallback, Embedded Art"
else
    echo "[ERROR] Invalid mode. Use 'dl' for DJ Mode."
    exit 1
fi

CMD_FLAGS="dl -D"

if command -v uv &> /dev/null; then
    echo "[INFO] Using uv..."
    uv run python -m qobuz_dl $CMD_FLAGS "$@"
    exit $?
fi

echo "[INFO] uv not found. Trying mamba..."
if command -v mamba &> /dev/null; then
    # Try using uv inside mamba environment 'qobuz'
    echo "[INFO] Attempting to run with uv inside mamba env 'qobuz'..."
    mamba run -n qobuz uv run python -m qobuz_dl $CMD_FLAGS "$@" 2>/dev/null
    if [ $? -eq 0 ]; then
        exit 0
    fi
    
    # Fallback to direct execution in mamba
    echo "[INFO] uv failed inside mamba. Attempting to run qobuz-dl directly inside mamba env 'qobuz'..."
    mamba run -n qobuz python -m qobuz_dl $CMD_FLAGS "$@"
    exit $?
fi

echo "[INFO] mamba not found. Trying qobuz-dl directly..."
python -m qobuz_dl $CMD_FLAGS "$@"
