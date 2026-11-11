#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")/.."

pdm run autoflake .
pdm run isort .
pdm run black .
