#!/bin/bash
for f in FUN_800131a8 FUN_80012820 FUN_8003c340 FUN_8004486c FUN_8004a090; do
  echo "== $f =="
  bash verificar.sh "$f"
done
