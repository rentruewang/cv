#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")/.."

pdm config python.use_venv true
pdm install -G:all
