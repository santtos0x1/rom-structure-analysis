import csv
import shutil
from pathlib import Path
import argparse

def unique_name(folder, base_name):
    path = folder / base_name
    counter = 1

    while path.exists():
        name, ext = base_name.rsplit(".", 1)
        path = folder / f"{name}_{counter}.{ext}"
        counter += 1

    return path

def resolve_file(base_dir, file_name, root):
    file_path = Path(file_name)

    # 1. absolute path
    if file_path.is_absolute() and file_path.exists():
        return file_path

    # 2. relative to report.csv folder
    candidate = (base_dir / file_path).resolve()
    if candidate.exists():
        return candidate

    # 3. relative to project root
    candidate = (root / file_path).resolve()
    if candidate.exists():
        return candidate

    # 4. brute-force search by filename
    matches = list(root.rglob(file_path.name))
    if matches:
        return matches[0]

    return None

def main():
    parser = argparse.ArgumentParser(description="Organize files from report.csv")
    parser.add_argument("input", help="Root folder")
    args = parser.parse_args()

    root = Path(args.input)

    out_audio = root / "audio_wav"
    out_noise = root / "noise_wav"
    out_data  = root / "data_wav"

    out_audio.mkdir(exist_ok=True)
    out_noise.mkdir(exist_ok=True)
    out_data.mkdir(exist_ok=True)

    reports = list(root.rglob("report.csv"))

    if not reports:
        print("No report.csv found.")
        return

    for report in reports:
        base_dir = report.parent
        print(f"\n[+] Processing: {report}")

        with open(report, newline='') as f:
            reader = csv.DictReader(f)

            for row in reader:
                file_name = row.get("file", "").strip()
                file_class = row.get("class", "").strip().lower()

                if not file_name or not file_class:
                    continue

                original_file = resolve_file(base_dir, file_name, root)

                if original_file is None or not original_file.exists():
                    print(f"[!] Missing file: {file_name}")
                    continue

                if file_class == "audio":
                    dest_folder = out_audio
                elif file_class == "noise":
                    dest_folder = out_noise
                elif file_class == "data":
                    dest_folder = out_data
                else:
                    continue

                dest = unique_name(dest_folder, original_file.name)
                shutil.copy2(original_file, dest)

                print(f"[+] {original_file} -> {file_class} -> {dest.name}")

    print("\nDone.")

if __name__ == "__main__":
    main()