
import os

from config import DATASET_ROOT, NUM_MODELS, ALL_FILES
from utils  import out


def run():
    lines = [
        "SHREC 2020 Cryo-ET Dataset – Structure Report",
        "=" * 52,
        "",
    ]
    total_files   = 0
    missing_files = []

    for m in range(NUM_MODELS):
        mdir   = os.path.join(DATASET_ROOT, f"model_{m}")
        exists = os.path.isdir(mdir)
        lines.append(f"model_{m}/  {'[EXISTS]' if exists else '[MISSING DIR]'}")

        if not exists:
            missing_files.append(f"model_{m}/ directory missing")
            lines.append("")
            continue

        found = sorted(os.listdir(mdir))
        for fname in found:
            fpath = os.path.join(mdir, fname)
            size_mb = os.path.getsize(fpath) / 1024 / 1024
            lines.append(f"   {fname:<35}  {size_mb:>8.2f} MB")
            total_files += 1

        for expected in ALL_FILES:
            if expected not in found:
                missing_files.append(f"model_{m}/{expected}")

        lines.append("")

    lines += [
        "-" * 52,
        f"Total files found : {total_files}",
        f"Missing files     : {len(missing_files)}",
    ]
    if missing_files:
        lines.append("Missing file list:")
        for mf in missing_files:
            lines.append(f"  - {mf}")

    dest = out("dataset_summary", "dataset_structure.txt")
    with open(dest, "w") as fh:
        fh.write("\n".join(lines))
    print(f"  ✔  Dataset structure saved → {dest}")
