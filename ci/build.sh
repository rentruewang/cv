#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")/.."

export PYTHONPATH=.
pdm run python main.py
