"""Convierte notas/ghidra/<exe>/funciones.tsv (formato direccion\\ttamano\\tnombre) al
formato que splat espera para symbol_addrs_path: NOMBRE = 0xDIRECCION;
Solo incluye direcciones en el rango del ejecutable (0x8xxxxxxx), descarta los macros
sinteticos del GTE (0x2xxxxxxx) que agrega el cargador de Ghidra.
"""
import sys

entrada, salida = sys.argv[1], sys.argv[2]
filas = []
with open(entrada, encoding="utf-8") as f:
    for linea in f:
        addr, _tam, nombre = linea.rstrip("\n").split("\t")
        if not addr.startswith("8"):
            continue
        filas.append((int(addr, 16), nombre))

filas.sort()
vistos = {}
with open(salida, "w", encoding="utf-8") as f:
    for addr, nombre in filas:
        if nombre in vistos:
            # nombre repetido (Ghidra encontro el mismo patron de libreria en dos sitios):
            # desambiguar con la direccion en vez de pisar el symbol_addrs de splat.
            nombre = f"{nombre}_{addr:08x}"
        vistos[nombre] = addr
        f.write(f"{nombre} = 0x{addr:08X};\n")

print(f"{len(filas)} simbolos escritos en {salida}")
