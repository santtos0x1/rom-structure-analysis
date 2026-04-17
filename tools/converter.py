import csv
import argparse

parser = argparse.ArgumentParser(description="Convert CSV ROM dump to BIN")
parser.add_argument("input", help="Path to input CSV file")
parser.add_argument("output", help="Path to output BIN file")
args = parser.parse_args()

data_bytes = []

with open(args.input) as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw = row["DATA"].strip()
        value = int(raw, 16)
        data_bytes.extend(value.to_bytes(2, byteorder='big'))

print(len(data_bytes))

with open(args.output, "wb") as f:
    f.write(bytearray(data_bytes))