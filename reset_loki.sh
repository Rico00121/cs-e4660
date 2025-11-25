#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "Stopping and removing existing Loki container..."
docker-compose stop loki || true
docker-compose rm -f loki || true

echo "Starting all containers..."
docker-compose up -d

echo "Loki reset complete."

