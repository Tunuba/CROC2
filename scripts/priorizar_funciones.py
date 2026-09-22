import re
import sys

base = "notas/ghidra/croc2exe"

# Parse decompilado.c to know which functions Ghidra could/couldn't decompile
fallidas = set()
with open(f"{base}/decompilado.c", encoding="utf-8", errors="replace") as f:
    current = None
    for line in f:
        m = re.match(r"// ==== (\S+) @ (\w+)", line)
        if m:
            current = m.group(1)
        elif "no se pudo decompilar" in line and current:
            fallidas.add(current)

filas = []
with open(f"{base}/funciones.tsv", encoding="utf-8") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) != 3:
            continue
        addr, size, name = parts
        if not addr.startswith("8"):
            continue
        if not name.startswith("FUN_"):
            continue  # ya es libreria PSY-Q conocida
        size = int(size)
        limpio = name not in fallidas
        filas.append((size, addr, name, limpio))

filas.sort(key=lambda x: x[0])

with open("decomp/prioridad_croc2exe.tsv", "w", encoding="utf-8") as out:
    out.write("direccion\ttamano\tnombre_ghidra\tdecompila_limpio\testado\n")
    for size, addr, name, limpio in filas:
        out.write(f"{addr}\t{size}\t{name}\t{'si' if limpio else 'no'}\tSIN_EMPEZAR\n")

print(f"{len(filas)} funciones candidatas en CROC2.EXE, ordenadas de mas facil a mas dificil.")
print(f"Primeras 10 (mas chicas): {[f[2] for f in filas[:10]]}")
print(f"Decompilan limpio (sin errores de Ghidra): {sum(1 for f in filas if f[3])}")
print(f"Decompilan con error/fallo: {sum(1 for f in filas if not f[3])}")
