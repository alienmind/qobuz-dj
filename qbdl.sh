#!/bin/bash

MODE="$1"
shift

if [ "$MODE" == "dla" ]; then
    CMD_FLAGS="dl -q 5 --no-fallback -s --no-db"
    echo "[INFO] Mode: Artist/Album (Smart Discography, No Flattening)"
elif [ "$MODE" == "dlp" ]; then
    CMD_FLAGS="dl -q 5 --no-fallback --no-db --folder-format ."
    echo "[INFO] Mode: Playlist (Flattening, No Smart Discography)"
else
    echo "[ERROR] Invalid mode. Use 'dla' for Artist/Album or 'dlp' for Playlist."
    exit 1
fi

if command -v uv &> /dev/null; then
    echo "[INFO] Using uv..."
    uv run qobuz-dl $CMD_FLAGS "$@"
    exit $?
fi

echo "[INFO] uv not found. Trying mamba..."
if command -v mamba &> /dev/null; then
    # Try using uv inside mamba environment 'qobuz'
    echo "[INFO] Attempting to run with uv inside mamba env 'qobuz'..."
    mamba run -n qobuz uv run qobuz-dl $CMD_FLAGS "$@" 2>/dev/null
    if [ $? -eq 0 ]; then
        exit 0
    fi
    
    # Fallback to direct execution in mamba
    echo "[INFO] uv failed inside mamba. Attempting to run qobuz-dl directly inside mamba env 'qobuz'..."
    mamba run -n qobuz qobuz-dl $CMD_FLAGS "$@"
    exit $?
fi

echo "[INFO] mamba not found. Trying qobuz-dl directly..."
qobuz-dl $CMD_FLAGS "$@"
