import csv

data_bytes = []

with open("rom_dump_16bit_final.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw = row["data"].strip()
        value = int(raw, 16)
        data_bytes.extend(value.to_bytes(2, byteorder='big'))

print(len(data_bytes))

with open("rom.bin", "wb") as f:
    f.write(bytearray(data_bytes))
