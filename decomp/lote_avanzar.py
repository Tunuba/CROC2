#!/usr/bin/env python3
# Recorre las funciones SIN_EMPEZAR de progreso.tsv en orden, genera un borrador de m2c si
# hace falta, intenta verificar, y guarda el resultado en progreso.tsv DESPUES DE CADA UNA
# (no en lotes), tal como pidio Meme. No corrige nada a mano: solo corre lo automatico y
# clasifica el resultado real. Correr dentro de WSL, con el venv activado, desde decomp/.
import re
import subprocess
import sys
import os

TSV = "progreso.tsv"
LIMITE = int(sys.argv[1]) if len(sys.argv) > 1 else 60


def leer():
    with open(TSV, encoding="utf-8") as f:
        lineas = [l.rstrip("\n") for l in f]
    header = lineas[0].split("\t")
    filas = [l.split("\t") for l in lineas[1:] if l]
    return header, filas


def escribir(header, filas):
    with open(TSV, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(header) + "\n")
        for fila in filas:
            f.write("\t".join(fila) + "\n")


def clasificar_no_compila(salida):
    if "NO_COMPILA (cpp)" in salida:
        motivo = "cpp"
    elif "NO_COMPILA (cc1)" in salida:
        motivo = "cc1"
    elif "NO_COMPILA (as)" in salida:
        motivo = "as"
    elif "NO_COMPILA (ld)" in salida:
        motivo = "ld"
    else:
        motivo = "?"
    lineas = [l for l in salida.strip().splitlines() if l.strip()]
    # cc1-27 (gcc 2.7 viejo) no siempre dice "error:"/"warning:" como el gcc moderno: una linea
    # real de error trae "archivo.c:NUMERO:", una de puro contexto es "archivo.c: In function"
    # (sin numero) y el ruido final es "for each function it appears in.)". Prefiere una linea
    # con numero que no sea warning; si todas son warnings, usa la ultima con numero.
    con_numero = [l for l in lineas if re.search(r"\.c:\d+:", l)]
    error = next((l for l in con_numero if "warning:" not in l), None)
    if error is None:
        error = con_numero[-1] if con_numero else (lineas[-1] if lineas else "")
    detalle = error[:160]
    return f"NO_COMPILA ({motivo}): {detalle}"


def procesar(nombre):
    src = f"src/croc2exe/{nombre}.c"
    if not os.path.exists(src):
        r = subprocess.run(
            ["bash", "generar_borrador.sh", nombre],
            capture_output=True, text=True, timeout=60,
        )
        if r.returncode != 0 or not os.path.exists(src):
            log = f"src/croc2exe/{nombre}.c.m2c.log"
            detalle = ""
            if os.path.exists(log):
                with open(log, encoding="utf-8", errors="replace") as f:
                    contenido = f.read().strip().splitlines()
                detalle = contenido[-1][:160] if contenido else ""  # log vacio: bug real, no IndexError
            return "NO_COMPILA", f"m2c no genero borrador: {detalle or r.stderr[:160]}"

    try:
        r = subprocess.run(
            ["bash", "verificar.sh", nombre],
            capture_output=True, text=True, timeout=45,
        )
    except subprocess.TimeoutExpired:
        return "NO_COMPILA", "verificar.sh se colgo mas de 45s (revisar a mano)"

    salida = r.stdout + r.stderr
    if salida.strip().startswith("IGUAL"):
        return "IGUAL", ""
    if "DISTINTO" in salida:
        return "DISTINTO", "bytes distintos, ver build/verificar/" + nombre + ".*"
    if "NO_COMPILA" in salida:
        return "NO_COMPILA", clasificar_no_compila(salida)
    if "SIN_DIRECCION" in salida:
        return "NO_COMPILA", "sin direccion en config/symbols.croc2exe.txt"
    return "NO_COMPILA", ("salida no reconocida: " + salida.strip()[:160])


def main():
    header, filas = leer()
    idx_nombre = header.index("nombre_ghidra")
    idx_estado = header.index("estado")
    idx_nota = header.index("nota") if "nota" in header else None

    procesadas = 0
    resumen = {}
    for fila in filas:
        if procesadas >= LIMITE:
            break
        if fila[idx_estado] != "SIN_EMPEZAR":
            continue
        nombre = fila[idx_nombre]
        try:
            estado, nota = procesar(nombre)
        except Exception as e:
            estado, nota = "NO_COMPILA", f"excepcion del driver: {e}"[:160]

        fila[idx_estado] = estado
        if idx_nota is not None:
            if len(fila) <= idx_nota:
                fila += [""] * (idx_nota + 1 - len(fila))
            fila[idx_nota] = nota
        escribir(header, filas)  # guardar YA, no al final

        procesadas += 1
        resumen[estado] = resumen.get(estado, 0) + 1
        print(f"[{procesadas}/{LIMITE}] {nombre}: {estado}" + (f" -- {nota}" if nota else ""))

    print("---")
    print("resumen de esta tanda:", resumen)


if __name__ == "__main__":
    main()
