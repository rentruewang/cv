#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")/.."

pdm run mypy .
