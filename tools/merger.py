import pandas as pd
import numpy as np
import argparse

def load_clean(path):
    rows = []
    with open(path, 'rb') as f:
        for line in f:
            line = line.replace(b'\r', b'').decode('utf-8', errors='ignore').strip()
            if line.lower().startswith('0x') and ',' in line:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) == 2:
                    try:
                        rows.append((int(parts[0], 16), int(parts[1], 16)))
                    except ValueError:
                        pass
    df = pd.DataFrame(rows, columns=['ADDR', 'DATA'])
    df = df.drop_duplicates(subset='ADDR', keep='first')
    return df.sort_values('ADDR').reset_index(drop=True)


parser = argparse.ArgumentParser(description="Merge LSB and MSB ROM dumps into 16-bit CSV")
parser.add_argument("lsb", help="Path to LSB CSV file")
parser.add_argument("msb", help="Path to MSB CSV file")
parser.add_argument("output", help="Output CSV file")
args = parser.parse_args()


lsb = load_clean(args.lsb)
msb = load_clean(args.msb)

merged = pd.merge(lsb, msb, on='ADDR', suffixes=('_LSB', '_MSB'), how='outer') \
           .sort_values('ADDR') \
           .reset_index(drop=True)

merged['DATA_LSB'] = merged['DATA_LSB'].fillna(0).astype(np.int64)
merged['DATA_MSB'] = merged['DATA_MSB'].fillna(0).astype(np.int64)
merged['DATA16']   = (merged['DATA_MSB'].values << 8) | merged['DATA_LSB'].values


with open(args.output, 'w') as f:
    f.write('ADDR,DATA\n')
    for _, row in merged.iterrows():
        f.write(f"0x{int(row['ADDR']):04X},0x{int(row['DATA16']):04X}\n")


print(f"Generated: {len(merged)}")