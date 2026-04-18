import numpy as np
import wave
import argparse
import os
import csv
from pathlib import Path

def load_wav(path):
    with wave.open(str(path), 'rb') as w:
        sr = w.getframerate()
        raw = w.readframes(w.getnframes())
    data = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    return data, sr

def basic_metrics(data):
    data = data - data.mean()

    std = np.std(data)
    if std < 1:
        return {"class": "silence"}

    autocorr = np.corrcoef(data[:-1], data[1:])[0,1]

    hist, _ = np.histogram(data, bins=64)
    p = hist / (np.sum(hist) + 1e-9)
    entropy = -np.sum(p[p > 0] * np.log2(p[p > 0]))

    return {
        "std": std,
        "autocorr": autocorr,
        "entropy": entropy
    }

def classify(m):
    if "class" in m:
        return "silence"
    if m["entropy"] > 7:
        return "data"
    if m["autocorr"] < 0.3:
        return "noise"
    return "audio"

def estimate_f0(data, sr):
    data = data * np.hanning(len(data))
    fft = np.abs(np.fft.rfft(data))
    freqs = np.fft.rfftfreq(len(data), 1/sr)

    fft[freqs < 50] = 0

    if np.max(fft) == 0:
        return 0

    return freqs[np.argmax(fft)]

def analyze(path):
    try:
        data, sr = load_wav(path)
    except:
        return None

    m = basic_metrics(data)
    c = classify(m)

    f0 = 0
    if c == "audio":
        f0 = estimate_f0(data, sr)

    return {
        "file": str(path),
        "class": c,
        "std": round(m.get("std",0),1),
        "autocorr": round(m.get("autocorr",0),3),
        "entropy": round(m.get("entropy",0),2),
        "f0": round(f0,1)
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Folder or file")
    parser.add_argument("--out", default="report.csv", help="Output CSV file")
    args = parser.parse_args()

    p = Path(args.input)

    if p.is_file():
        files = [p]
    else:
        files = list(p.rglob("*.wav"))  # 🔥 recursive

    results = []

    for f in files:
        r = analyze(f)
        if r:
            results.append(r)
            print(f"[+] {r['file']} -> {r['class']}")

    # save report
    if results:
        keys = results[0].keys()
        with open(args.out, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)

        print(f"\nReport saved to: {args.out}")
    else:
        print("No valid audio files found.")

if __name__ == "__main__":
    main()