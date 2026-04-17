import struct
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="Plot ROM binary data")
parser.add_argument("input", help="Path to input binary file")
parser.add_argument("output_prefix", help="Prefix for output images")
parser.add_argument("--size", type=int, default=4096, help="Bytes to read (default: 4096)")
args = parser.parse_args()

samples = []
addresses = []

with open(args.input, "rb") as f:
    raw = f.read(args.size)

for i in range(0, len(raw), 2):
    sample = struct.unpack(">H", raw[i:i+2])[0]
    samples.append(sample)
    addresses.append(i)

for i in range(0, len(samples), 100):
    subset_samples = samples[i:i+100]
    subset_addr = addresses[i:i+100]

    plt.figure()

    plt.plot(subset_addr, subset_samples, marker='o')

    plt.xlabel("Address (hex)")
    plt.ylabel("Value")
    plt.title(f"ROM Data ({i*2} to {(i+100)*2})")

    for x, y in zip(subset_addr, subset_samples):
        plt.vlines(x=x, ymin=0, ymax=y)

    plt.tight_layout()
    plt.savefig(f"{i}_normalized_sample_data_{args.output_prefix}.jpeg")
    plt.close()

print("Done!")