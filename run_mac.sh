#!/usr/bin/env bash
# run_mac.sh - double-click friendly runner for macOS/Linux (or run from terminal)
set -e
cd "$(dirname "$0")"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 run.py