import struct
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="Histogram of ROM data")
parser.add_argument("input", help="Path to input binary file")
parser.add_argument("--size", type=int, default=4096, help="Bytes to read")
parser.add_argument("--bins", type=int, default=100, help="Number of histogram bins")
args = parser.parse_args()

samples = []

# read binary
with open(args.input, "rb") as f:
    raw = f.read(args.size)

# decode 16-bit samples
for i in range(0, len(raw), 2):
    sample = struct.unpack(">H", raw[i:i+2])[0]
    samples.append(sample)

# plot histogram
plt.figure()
plt.hist(samples, bins=args.bins)

plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("ROM Data Histogram")

plt.tight_layout()
plt.savefig("histogram.jpeg")
plt.show()

print("Histogram generated.")