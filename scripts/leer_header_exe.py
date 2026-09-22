import struct

with open("extraido/SLUS_006.34", "rb") as f:
    data = f.read(0x800)

magic = data[0:8]
pc0, gp0, t_addr, t_size, d_addr, d_size, b_addr, b_size, s_addr, s_size = struct.unpack(
    "<10I", data[0x10:0x38]
)
print("magic:", magic)
print(f"pc0    = 0x{pc0:08X}")
print(f"gp0    = 0x{gp0:08X}")
print(f"t_addr = 0x{t_addr:08X}")
print(f"t_size = 0x{t_size:08X} ({t_size})")
print(f"d_addr = 0x{d_addr:08X}")
print(f"d_size = 0x{d_size:08X}")
print(f"b_addr = 0x{b_addr:08X}")
print(f"b_size = 0x{b_size:08X}")
print(f"s_addr = 0x{s_addr:08X}")
print(f"s_size = 0x{s_size:08X}")
