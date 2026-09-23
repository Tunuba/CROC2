#!/usr/bin/env python3
# Reinicia a SIN_EMPEZAR las filas que quedaron mal clasificadas por bugs ya corregidos en
# lote_avanzar.py: la excepcion "list index out of range" (log vacio) y la nota que capturaba
# la linea de ruido de cc1 en vez del error real. Se corre una sola vez.
TSV = "progreso.tsv"
PATRONES_MALOS = [
    "excepcion del driver: list index out of range",
]
FRAGMENTOS_RUIDO = [
    "for each function it appears in",
    "control reaches end of non-void function",
]

with open(TSV, encoding="utf-8") as f:
    lineas = [l.rstrip("\n") for l in f]

header = lineas[0].split("\t")
idx_estado = header.index("estado")
idx_nota = header.index("nota")

reiniciadas = 0
filas = []
for l in lineas[1:]:
    if not l:
        continue
    fila = l.split("\t")
    nota = fila[idx_nota] if len(fila) > idx_nota else ""
    if nota in PATRONES_MALOS or any(frag in nota for frag in FRAGMENTOS_RUIDO):
        fila[idx_estado] = "SIN_EMPEZAR"
        fila[idx_nota] = ""
        reiniciadas += 1
    filas.append(fila)

with open(TSV, "w", encoding="utf-8", newline="\n") as f:
    f.write("\t".join(header) + "\n")
    for fila in filas:
        f.write("\t".join(fila) + "\n")

print(f"reiniciadas: {reiniciadas}")
