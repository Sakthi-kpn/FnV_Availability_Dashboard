#!/usr/bin/env python3
"""Download the published 'Extract 1' CSV (Google Sheets -> File -> Share -> Publish to web)
and save it as data/daily/FnV_YYYY-MM-DD.csv when it holds a day we don't have yet.
Writes new=true/false to $GITHUB_OUTPUT."""
import os, sys, io, urllib.request
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
cfg = os.path.join(HERE, 'config', 'sheet_csv_url.txt')
out_flag = os.environ.get('GITHUB_OUTPUT')

def flag(v):
    if out_flag:
        with open(out_flag, 'a') as f: f.write(f'new={v}\n')

if not os.path.exists(cfg) or not open(cfg).read().strip():
    print('No config/sheet_csv_url.txt - skipping sheet fetch'); flag('false'); sys.exit(0)
url = open(cfg).read().strip().split()[0]

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
raw = urllib.request.urlopen(req, timeout=60).read().decode('utf-8-sig')
df = pd.read_csv(io.StringIO(raw))
df.columns = [str(c).strip() for c in df.columns]
need = ['outlet_id', 'dt', 'ksin', 'total_sku_hours', 'total_store_hrs']
if any(c not in df.columns for c in need) or df.empty:
    print('Published sheet does not look like Extract 1:', df.columns.tolist()[:10]); flag('false'); sys.exit(0)

df = df[df['outlet_id'].astype(str).str.strip() != '']
df['dt'] = pd.to_datetime(df['dt'], errors='coerce').dt.strftime('%Y-%m-%d')
df = df.dropna(subset=['dt'])
os.makedirs(os.path.join(HERE, 'data', 'daily'), exist_ok=True)

# The sheet may hold one day or several (e.g. last 3 days). Save every day we don't have yet,
# or that now has more rows than before, so a missed refresh day is recovered later.
saved = []
for day, part in sorted(df.groupby('dt')):
    path = os.path.join(HERE, 'data', 'daily', f'FnV_{day}.csv')
    if os.path.exists(path) and len(pd.read_csv(path)) >= len(part):
        print(f'{day} already saved ({len(part)} rows)'); continue
    part.to_csv(path, index=False); saved.append(day)
    print(f'Saved {path} ({len(part)} rows)')
flag('true' if saved else 'false')
