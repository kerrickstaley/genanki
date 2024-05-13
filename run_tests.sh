#!/bin/bash
# TODO make this cleaner / platform-independent
set -e

# enter venv if needed
[[ -z "$VIRTUAL_ENV" ]] && source tests_venv/bin/activate

exec python -m pytest tests/
