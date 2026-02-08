#!/bin/bash

PARAMS="$@"
echo "qbdl is a handy downloader using qobuz-dl with common options for DJs"
CMD_FLAGS="dl -q 5 --no-fallback -s --no-db --folder-format ."

if command -v uv &> /dev/null; then
    echo "[INFO] Using uv..."
    uv run qobuz-dl $CMD_FLAGS $PARAMS
    exit $?
fi

echo "[INFO] uv not found. Trying mamba..."
if command -v mamba &> /dev/null; then
    # Try using uv inside mamba environment 'qobuz'
    echo "[INFO] Attempting to run with uv inside mamba env 'qobuz'..."
    mamba run -n qobuz uv run qobuz-dl $CMD_FLAGS $PARAMS 2>/dev/null
    if [ $? -eq 0 ]; then
        exit 0
    fi
    
    # Fallback to direct execution in mamba
    echo "[INFO] uv failed inside mamba. Attempting to run qobuz-dl directly inside mamba env 'qobuz'..."
    mamba run -n qobuz qobuz-dl $CMD_FLAGS $PARAMS
    exit $?
fi

echo "[INFO] mamba not found. Trying qobuz-dl directly..."
qobuz-dl $CMD_FLAGS $PARAMS
