
import os
import numpy as np
import pandas as pd

from config import DATASET_ROOT, NUM_MODELS, VOLUME_FILES
from utils  import load_mrc, out


def run():
    rows = []

    for m in range(NUM_MODELS):
        for vf in VOLUME_FILES:
            path = os.path.join(DATASET_ROOT, f"model_{m}", vf)
            if not os.path.isfile(path):
                continue
            try:
                vol = load_mrc(path)
                rows.append({
                    "model":       f"model_{m}",
                    "file":        vf,
                    "shape_Z":     vol.shape[0],
                    "shape_Y":     vol.shape[1] if vol.ndim >= 2 else 1,
                    "shape_X":     vol.shape[2] if vol.ndim >= 3 else 1,
                    "mean":        round(float(np.mean(vol)),  6),
                    "std":         round(float(np.std(vol)),   6),
                    "min":         round(float(np.min(vol)),   6),
                    "max":         round(float(np.max(vol)),   6),
                    "voxel_count": int(vol.size),
                })
            except Exception as e:
                rows.append({
                    "model": f"model_{m}",
                    "file":  vf,
                    "error": str(e),
                })

    df   = pd.DataFrame(rows)
    dest = out("dataset_summary", "volume_statistics.csv")
    df.to_csv(dest, index=False)
    print(f"  ✔  Volume statistics saved → {dest}  ({len(rows)} rows)")
    return df
