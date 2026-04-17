import pandas as pd
import numpy as np

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


lsb = load_clean('../rom_dump_lsb_0000010.csv')
msb = load_clean('../rom_dump_msb_0000010.csv')

merged = pd.merge(lsb, msb, on='ADDR', suffixes=('_LSB', '_MSB'), how='outer').sort_values('ADDR').reset_index(drop=True)
merged['DATA_LSB'] = merged['DATA_LSB'].fillna(0).astype(np.int64)
merged['DATA_MSB'] = merged['DATA_MSB'].fillna(0).astype(np.int64)
merged['DATA16']   = (merged['DATA_MSB'].values << 8) | merged['DATA_LSB'].values

with open('dump_16bit_0000010.csv', 'w') as f:
    f.write('ADDR,DATA\n')
    for _, row in merged.iterrows():
        f.write(f"0x{int(row['ADDR']):04X},0x{int(row['DATA16']):04X}\n")

print(f"Generated: {len(merged)}")