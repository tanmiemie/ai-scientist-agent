#!/usr/bin/env bash
# Leakage and determinism tests. Usage: bash run_tests.sh  (pack next to this folder, or GPU_PACK=/path/to/pack)
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
exec "${PYTHON:-python3}" -m pytest tests -v -p no:cacheprovider "$@"
