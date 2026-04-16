import struct
import matplotlib.pyplot as plt

samples = []

with open("rom.bin", "rb") as f:
    raw = f.read(4096)

for i in range(0, len(raw), 2):
    sample = struct.unpack(">H", raw[i:i+2])[0]  # try "<H" too
    samples.append(sample)

plt.plot(samples[:1000])
plt.show()
