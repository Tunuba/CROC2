#!/bin/bash
# Verifica una funcion de src/croc2exe/$1.c contra el original en
# asm/croc2exe/nonmatchings/800/$1.s, comparando los bytes de verdad (no solo el texto del
# desensamblado). Correr dentro de WSL, con el venv activado, desde decomp/.
set -e
FUNC=$1
ORIG=asm/croc2exe/nonmatchings/800/$FUNC.s
SRC=src/croc2exe/$FUNC.c
OUT=build/verificar
mkdir -p $OUT

if [ ! -f "$ORIG" ]; then echo "NO_EXISTE: $ORIG"; exit 1; fi
if [ ! -f "$SRC" ]; then echo "NO_EXISTE: $SRC"; exit 1; fi

# Enlazar cada funcion en su direccion REAL, no una generica: un salto tipo j/jal a una
# etiqueta local (ej. un loop "j si_mismo") codifica bits que dependen de donde vive de
# verdad la funcion, no solo de direcciones externas absolutas (esas si dan igual donde se
# linkee). Sacamos la direccion de symbols.croc2exe.txt.
ADDR=$(grep -E "^$FUNC = " config/symbols.croc2exe.txt | head -1 | grep -oE '0x[0-9A-Fa-f]+')
if [ -z "$ADDR" ]; then echo "SIN_DIRECCION: $FUNC no esta en config/symbols.croc2exe.txt"; exit 1; fi
# Comprobado a mano (probar_addr.sh): ld coloca .text exactamente en la direccion pedida sin
# redondear a 16, siempre que sea multiplo de 4 (todo el codigo MIPS lo es). El "relleno" que
# se restaba antes no existia de verdad: solo recortaba bytes reales de funciones chicas.
sed "s/0x90000000/$ADDR/" verificar.ld > "$OUT/$FUNC.ld"

CPP_FLAGS="-Iinclude -Iinclude/psyq -undef -Wall -lang-c -fno-builtin -Dmips -D__GNUC__=2 -D__OPTIMIZE__ -D__mips__ -D__mips -Dpsx -D__psx__ -D__psx -D_PSYQ -D__EXTENSIONS__ -D_MIPSEL -D_LANGUAGE_C -DLANGUAGE_C"
CC_FLAGS="-mips1 -mcpu=3000 -quiet -G0 -Wall -fno-builtin -mno-abicalls -funsigned-char -O1"
AS_FLAGS="-Iinclude -march=r3000 -mtune=r3000 -no-pad-sections -O1"

mipsel-linux-gnu-cpp $CPP_FLAGS "$SRC" > "$OUT/$FUNC.i" 2>"$OUT/$FUNC.cpp.log" || { echo "NO_COMPILA (cpp)"; cat "$OUT/$FUNC.cpp.log"; exit 1; }
./bin/cc1-27 $CC_FLAGS "$OUT/$FUNC.i" -o "$OUT/$FUNC.s" 2>"$OUT/$FUNC.cc1.log" || { echo "NO_COMPILA (cc1)"; cat "$OUT/$FUNC.cc1.log"; exit 1; }
python3 ~/decomp-herramientas/maspsx/maspsx.py --expand-div --aspsx-version=2.56 "$OUT/$FUNC.s" > "$OUT/$FUNC.fixed.s" 2>/dev/null
mipsel-linux-gnu-as $AS_FLAGS -o "$OUT/$FUNC.o" "$OUT/$FUNC.fixed.s" 2>"$OUT/$FUNC.as.log" || { echo "NO_COMPILA (as)"; cat "$OUT/$FUNC.as.log"; exit 1; }
mipsel-linux-gnu-ld -o "$OUT/$FUNC.elf" -T "$OUT/$FUNC.ld" -T config/symbols.croc2exe.txt -T config/undefined_syms_auto.croc2exe.txt --no-check-sections -nostdlib "$OUT/$FUNC.o" 2>"$OUT/$FUNC.ld.log" || { echo "NO_COMPILA (ld)"; cat "$OUT/$FUNC.ld.log"; exit 1; }

# bytes nuestros: seccion .text del elf de prueba, completa (ya no hace falta recortar nada)
mipsel-linux-gnu-objcopy -O binary --only-section=.text "$OUT/$FUNC.elf" "$OUT/$FUNC.bin"
NUESTRO=$(xxd -p "$OUT/$FUNC.bin" | tr -d '\n')

# bytes originales: los que trae el .s de splat en los comentarios (palabra de 8 hex tras la direccion)
ORIGINAL=$(grep -oE '/\* [0-9A-Fa-f]+ [0-9A-Fa-f]+ [0-9A-Fa-f]{8} \*/' "$ORIG" | awk '{print $4}' | tr -d '\n' | tr 'A-F' 'a-f')

if [ "$NUESTRO" == "$ORIGINAL" ]; then
    echo "IGUAL"
else
    echo "DISTINTO"
    echo "nuestro:   $NUESTRO"
    echo "original:  $ORIGINAL"
fi
