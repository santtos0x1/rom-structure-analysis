import struct
import matplotlib.pyplot as plt

samples = []
addresses = []

with open("data/addr_0000001/rom_0000001.bin", "rb") as f:
    raw = f.read(4096)

for i in range(0, len(raw), 2):
    sample = struct.unpack(">H", raw[i:i+2])[0]
    samples.append(sample)
    addresses.append(i)  # real address (byte offset)

for i in range(0, 4001, 100):
    subset_samples = samples[i:i+100]
    subset_addr = addresses[i:i+100]
    
    plt.figure()

    plt.xlabel("Address (hex)")
    plt.ylabel("Value")
    plt.title(f"ROM Data ({i*2} to {(i+i+200)})")

    plt.plot(subset_addr, subset_samples, marker='o')

    for x, y in zip(subset_addr, subset_samples):
        plt.vlines(x=x, ymin=0, ymax=y, colors="red")
        #if y > 0:
        #    plt.text(x, y, f"{hex(x)}\n{y}", fontsize=7, ha='center', color="black")

    plt.savefig(f"{i}_normalized_sample_data200_0000001.jpeg");
    
print("Done!")