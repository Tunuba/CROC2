#!/bin/bash
for f in "$@"; do
  bash generar_borrador.sh "$f" 2>&1
done
