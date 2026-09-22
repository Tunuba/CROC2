import re

data = open("extraido/SLUS_006.34", "rb").read()
strs = re.findall(rb"[\x20-\x7e]{6,}", data)
keys = [
    b"psy", b"PSY", b"SN Sys", b"gcc", b"GCC", b"CodeWarrior", b"Metrowerks",
    b".obj", b".c", b"D:\\", b"C:\\", b"PROJECT", b"MWERKS", b"linker",
    b"compiler", b"ccpsx", b"asmpsx",
]
seen = set()
for s in strs:
    for k in keys:
        if k in s and s not in seen:
            seen.add(s)
            print(s.decode(errors="replace"))
            break
