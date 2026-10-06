#!/usr/bin/env bash
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"
export ABAQUS_CMD="${ABAQUS_CMD:-abaqus}"
exec "${PYTHON_BIN:-python3}" "$HERE/abaqus_postprocess_gui_linux.py"
