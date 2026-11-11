#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")"

bash formatting.sh
bash typing.sh
