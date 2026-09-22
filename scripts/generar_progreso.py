with open("notas/ghidra/funciones.tsv", encoding="utf-8") as f:
    filas = [l.rstrip("\n").split("\t") for l in f if l.startswith("8")]

candidatas = [(a, s, n) for a, s, n in filas if n.startswith("FUN_")]

with open("decomp/progreso.tsv", "w", encoding="utf-8") as f:
    f.write("direccion\ttamano\tnombre_ghidra\testado\n")
    for addr, size, name in candidatas:
        f.write(f"{addr}\t{size}\t{name}\tSIN_EMPEZAR\n")

print(f"{len(candidatas)} funciones candidatas en decomp/progreso.tsv")
