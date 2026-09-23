#!/bin/bash
for f in "$@"; do
  echo "== $f =="
  timeout 30 bash verificar.sh "$f" 2>&1 | head -6
done
