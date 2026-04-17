import numpy as np
import struct
import argparse
import wave
import os

def save_wav(samples, sr, path):
    samples = samples.astype(np.float64)
    samples = samples - samples.mean()
    samples = samples / (np.max(np.abs(samples)) + 1e-9)
    samples = (samples * 32767).astype(np.int16)

    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(samples.tobytes())

def decode_samples(raw, endian):
    samples = []
    for i in range(0, len(raw), 2):
        chunk = raw[i:i+2]
        if len(chunk) < 2:
            continue
        if endian == "be":
            val = struct.unpack(">H", chunk)[0]
        else:
            val = struct.unpack("<H", chunk)[0]

        val = val - 32768
        samples.append(val)

    return np.array(samples, dtype=np.int16)

def process_chunks(samples, chunk_size, repeat, step, sr, out_dir, max_files):
    os.makedirs(out_dir, exist_ok=True)
    count = 0

    for start in range(0, len(samples) - chunk_size, step):
        chunk = samples[start:start + chunk_size]

        # skip boring chunks
        if np.std(chunk) < 10:
            continue

        looped = np.tile(chunk, repeat)

        filename = os.path.join(out_dir, f"sample_{start}.wav")
        save_wav(looped, sr, filename)

        print(f"[{chunk_size}] Saved: {filename}")

        count += 1
        if count >= max_files:
            break

    print(f"Generated {count} samples for chunk {chunk_size}\n")


def main():
    parser = argparse.ArgumentParser(description="Extract audio candidates (64 & 128 chunks)")
    parser.add_argument("input", help="Input binary file")
    parser.add_argument("--repeat", type=int, default=1000)
    parser.add_argument("--step", type=int, default=64)
    parser.add_argument("--endian", choices=["be", "le"], default="be")
    parser.add_argument("--out", default="audio_out")
    parser.add_argument("--max", type=int, default=50)
    args = parser.parse_args()

    sr = 11025  # fixed

    with open(args.input, "rb") as f:
        raw = f.read()

    samples = decode_samples(raw, args.endian)

    # create base folder
    os.makedirs(args.out, exist_ok=True)

    # process 64
    process_chunks(
        samples,
        chunk_size=64,
        repeat=args.repeat,
        step=args.step,
        sr=sr,
        out_dir=os.path.join(args.out, "chunk_64"),
        max_files=args.max
    )

    # process 128
    process_chunks(
        samples,
        chunk_size=128,
        repeat=args.repeat,
        step=args.step,
        sr=sr,
        out_dir=os.path.join(args.out, "chunk_128"),
        max_files=args.max
    )

    print("Done. Organized like a civilized human.")

if __name__ == "__main__":
    main()