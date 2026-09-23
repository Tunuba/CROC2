#!/bin/bash
# Genera un borrador de m2c para una funcion si no existe ya src/croc2exe/$1.c
set -e
FUNC=$1
SRC=src/croc2exe/$FUNC.c
if [ -f "$SRC" ]; then echo "ya existe: $SRC"; exit 0; fi
echo '#include "common.h"' > "$SRC.tmp"
python3 ~/decomp-herramientas/m2c/m2c.py -P 4 --target mipsel-gcc-c "asm/croc2exe/nonmatchings/800/$FUNC.s" >> "$SRC.tmp" 2>"$SRC.m2c.log"
# m2c deja "?" como tipo de retorno cuando no lo puede inferir (en externs y a veces en la
# funcion misma); no es valido en C, cc1 tira "parse error before `?'". s32 generico, mismo
# criterio que el resto de tipos sin resolver en este proyecto.
sed -i -E 's/^\? /s32 /' "$SRC.tmp"
mv "$SRC.tmp" "$SRC"
echo "generado: $SRC"
