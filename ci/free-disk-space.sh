#!/usr/bin/env bash

set -euo pipefail

if [[ "${GITHUB_ACTIONS:-}" != "true" ]]; then
    echo "Not running in GitHub Actions, refusing to delete system files." >&2
    exit 1
fi

echo "Removing files we did not ask for..."
sudo rm -rf /usr/local/lib/android
sudo rm -rf /usr/share/dotnet
sudo rm -rf /usr/local/.ghcup
docker system prune -af --volumes

echo "Investigating how much storage is used in GitHub Actions..."
df -h
