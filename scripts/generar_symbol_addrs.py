import re

out_lines = []
with open("notas/ghidra/funciones.tsv", encoding="utf-8") as f:
    for line in f:
        addr, size, name = line.rstrip("\n").split("\t")
        if not addr.startswith("8"):
            continue  # nos quedamos solo con el rango del juego, no las macros GTE sinteticas
        name = re.sub(r"[^A-Za-z0-9_]", "_", name)
        if re.match(r"^\d", name):
            name = "_" + name
        out_lines.append(f"{name} = 0x{addr.upper()};")

with open("decomp/config/symbols.slus00634.croc2.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines) + "\n")

print(f"{len(out_lines)} simbolos escritos")
