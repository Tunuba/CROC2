import re

data = open("extraido/SLUS_006.34", "rb").read()
strs = re.findall(rb"[\x20-\x7e]{4,}", data)
for s in strs:
    if b"CROC2" in s.upper() or b".EXE" in s.upper() or b"CDROM" in s.upper():
        print(s.decode(errors="replace"))
