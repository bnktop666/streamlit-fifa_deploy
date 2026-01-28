import os
import re
import time
import pandas as pd
import requests
from urllib.parse import urlparse

CSV_PATH = "dataset/CLEAN_FIFA23_official_data.csv"   # ajuste
PHOTO_COL = "Photo"
OUT_DIR = "assets/photos"
SLEEP = 0.05  # 50ms entre requests pra não martelar o CDN

os.makedirs(OUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://sofifa.com/",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
}

def clean_url(u: str) -> str:
    u = str(u).replace("\u00a0", " ").strip()
    u = re.sub(r"\s+", "", u)  # remove qualquer whitespace
    return u

def make_filename(url: str) -> str:
    # cria nome estável: players_192_119_23_60.png
    p = urlparse(url).path.strip("/")
    return p.replace("/", "_")

def main():
    df = pd.read_csv(CSV_PATH)
    urls = (
        df[PHOTO_COL]
        .dropna()
        .astype(str)
        .map(clean_url)
        .unique()
        .tolist()
    )

    print(f"Total de URLs únicas: {len(urls)}")

    s = requests.Session()

    ok = 0
    fail = 0

    for i, url in enumerate(urls, start=1):
        if not url.startswith("http"):
            fail += 1
            continue

        fname = make_filename(url)
        out_path = os.path.join(OUT_DIR, fname)

        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            ok += 1
            continue  # já baixou

        try:
            r = s.get(url, headers=headers, timeout=20, allow_redirects=True)
            if r.status_code == 200 and (r.headers.get("Content-Type", "").lower().startswith("image/")):
                with open(out_path, "wb") as f:
                    f.write(r.content)
                ok += 1
            else:
                fail += 1
        except Exception:
            fail += 1

        if i % 200 == 0:
            print(f"{i}/{len(urls)} | ok={ok} fail={fail}")

        time.sleep(SLEEP)

    print("Final:", f"ok={ok}", f"fail={fail}")

if __name__ == "__main__":
    main()
