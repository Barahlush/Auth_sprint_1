#!/usr/bin/env bash
functional/utils/wait-for-it.sh redis:6379 --timeout=10 --strict -- \
  functional/utils/wait-for-it.sh nginx:80 --timeout=10 --strict -- \
  python -m pytest .