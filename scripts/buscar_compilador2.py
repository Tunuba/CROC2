import re

data = open("extraido/SLUS_006.34", "rb").read()
strs = re.findall(rb"[\x20-\x7e]{4,}", data)
keys = [b"gcc", b"GCC", b"2.7", b"2.8", b"cc1", b"as ", b"GNU", b"Id:", b"psyq", b"PSYQ"]
seen = set()
for s in strs:
    for k in keys:
        if k in s and s not in seen:
            seen.add(s)
            print(s.decode(errors="replace"))
            break
