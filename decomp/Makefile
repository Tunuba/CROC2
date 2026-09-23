# Pipeline de matching decomp para CROC2.EXE (el juego real; SLUS_006.34 es solo el cargador
# de 163 KB que lo carga desde el disco y le salta, no hace falta decompilarlo), calcado del de
# Xeeynamo/croc. Reusa las herramientas ya instaladas en WSL para Sabrina (m2c, maspsx,
# asm-differ, venv con splat64). Correr siempre dentro de WSL: wsl -d Ubuntu-24.04

PYTHON      := python3
CROSS       := mipsel-linux-gnu-
AS          := $(CROSS)as
CC          := ./bin/cc1-27
CPP         := $(CROSS)cpp
AS_FLAGS    += -Iinclude -march=r3000 -mtune=r3000 -no-pad-sections -O1
CC_FLAGS    += -mips1 -mcpu=3000 -quiet -G0 -Wall -fno-builtin -mno-abicalls -funsigned-char -O1
CPP_FLAGS   += -Iinclude -undef -Wall -lang-c -fno-builtin -gstabs
CPP_FLAGS   += -Dmips -D__GNUC__=2 -D__OPTIMIZE__ -D__mips__ -D__mips -Dpsx -D__psx__ -D__psx -D_PSYQ -D__EXTENSIONS__ -D_MIPSEL -D_LANGUAGE_C -DLANGUAGE_C

HERRAMIENTAS := $(HOME)/decomp-herramientas
MASPSX       := $(PYTHON) $(HERRAMIENTAS)/maspsx/maspsx.py --expand-div --aspsx-version=2.56
M2C          := $(PYTHON) $(HERRAMIENTAS)/m2c/m2c.py -P 4
ASMDIFFER    := $(PYTHON) $(HERRAMIENTAS)/asm-differ/diff.py

.PHONY: extract extract-loader all decompile check-compiler

extract:
	$(PYTHON) -m splat split config/splat.croc2exe.yml

# El cargador (SLUS_006.34) no hace falta decompilarlo, es 100% libreria PSY-Q conocida segun
# Ghidra; esto queda solo por si algun dia hace falta revisarlo de nuevo.
extract-loader:
	$(PYTHON) -m splat split config/splat.slus00634.croc2.yml

check-compiler:
	@test -x $(CC) || (echo "Falta $(CC): el compilador PSY-Q no se descarga solo, ver notas/TRASPASO.md seccion 'Bloqueo, el compilador'."; exit 1)

all: check-compiler
	@echo "Compilacion real pendiente de $(CC). Ver notas/TRASPASO.md."

# FUNC=nombre_funcion make decompile
decompile:
	$(M2C) --target mipsel-gcc-c asm/croc2exe/nonmatchings/800/$(FUNC).s
