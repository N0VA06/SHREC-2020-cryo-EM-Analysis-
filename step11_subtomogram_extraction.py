
import os
import numpy as np
import matplotlib.pyplot as plt

from config import (DATASET_ROOT, NUM_MODELS, PARTICLE_COLS,
                    CUBE_SIZE, CMAP_GRAY, CMAP_HEAT)
from utils  import load_mrc, save_fig, label_axes, add_colorbar, out


# ── Cube extraction ───────────────────────────────────────────────────────────

def _extract(vol: np.ndarray, x: float, y: float, z: float,
             size: int = CUBE_SIZE) -> np.ndarray:
    half = size // 2
    zi, yi, xi = int(round(z)), int(round(y)), int(round(x))

    z0, z1 = max(0, zi - half), min(vol.shape[0], zi + half)
    y0, y1 = max(0, yi - half), min(vol.shape[1], yi + half)
    x0, x1 = max(0, xi - half), min(vol.shape[2], xi + half)
    sub = vol[z0:z1, y0:y1, x0:x1]

    # Pad to exact CUBE_SIZE if near boundary
    pad = [
        (0, size - (z1 - z0)),
        (0, size - (y1 - y0)),
        (0, size - (x1 - x0)),
    ]
    return np.pad(sub, pad, mode="constant", constant_values=0)


# ── Particle file loader (same logic as step09 but kept local) ─────────────────

def _load_particles(path: str) -> "pd.DataFrame":
    import pandas as pd
    records = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 7:
                try:
                    records.append([float(v) for v in parts[:7]])
                except ValueError:
                    continue
    return pd.DataFrame(records, columns=PARTICLE_COLS) if records else \
           pd.DataFrame(columns=PARTICLE_COLS)


# ── Visual helper ─────────────────────────────────────────────────────────────

MAX_EXAMPLES_PER_CLASS = 3


def _examples_figure(df_class, vol: np.ndarray, cls_id: float, m: int):
    sample = df_class.head(MAX_EXAMPLES_PER_CLASS)
    ncols  = len(sample)
    fig, axes = plt.subplots(3, ncols, figsize=(ncols * 4, 10))
    if ncols == 1:
        axes = axes.reshape(3, 1)

    half = CUBE_SIZE // 2

    for col, (_, row) in enumerate(sample.iterrows()):
        xi, yi, zi = int(row["X"]), int(row["Y"]), int(row["Z"])
        sub = _extract(vol, row["X"], row["Y"], row["Z"])

        # Row 0 – original slice with particle marker
        ax0 = axes[0, col]
        sl  = vol[min(zi, vol.shape[0] - 1)]
        ax0.imshow(sl, cmap=CMAP_GRAY, origin="lower")
        ax0.plot(xi, yi, "r+", markersize=10, markeredgewidth=2)
        label_axes(ax0, f"Original slice Z={zi}")

        # Row 1 – central XY slice of extracted cube
        ax1 = axes[1, col]
        im1 = ax1.imshow(sub[CUBE_SIZE // 2], cmap=CMAP_GRAY, origin="lower")
        label_axes(ax1, "Subtomogram XY")
        add_colorbar(fig, ax1, im1)

        # Row 2 – zoomed region on the original slice
        ax2 = axes[2, col]
        y0, y1 = max(0, yi - half), min(vol.shape[1], yi + half)
        x0, x1 = max(0, xi - half), min(vol.shape[2], xi + half)
        zoom = sl[y0:y1, x0:x1]
        im2  = ax2.imshow(zoom, cmap=CMAP_HEAT, origin="lower")
        label_axes(ax2, "Zoomed Region")
        add_colorbar(fig, ax2, im2)

    fig.suptitle(
        f"model_{m} – Class {int(cls_id)} Subtomogram Examples",
        fontweight="bold",
    )
    save_fig(fig, "subtomograms", "subtomogram_examples",
             f"model_{m}_class{int(cls_id)}_examples.png")


# ── Public entry point ────────────────────────────────────────────────────────

def run():
    npy_dir = out("subtomograms", "extracted_particles")

    for m in range(NUM_MODELS):
        base  = os.path.join(DATASET_ROOT, f"model_{m}")
        gm_p  = os.path.join(base, "grandmodel.mrc")
        loc_p = os.path.join(base, "particle_locations.txt")

        if not (os.path.isfile(gm_p) and os.path.isfile(loc_p)):
            continue

        vol = load_mrc(gm_p)
        df  = _load_particles(loc_p)
        if df.empty:
            continue

        # Save .npy for the first 20 particles
        for idx, (_, row) in enumerate(df.head(20).iterrows()):
            sub = _extract(vol, row["X"], row["Y"], row["Z"])
            np.save(
                os.path.join(npy_dir, f"model_{m}_sub_{idx:04d}.npy"),
                sub,
            )

        # Visual examples per class
        for cls_id, grp in df.groupby("class_id"):
            _examples_figure(grp, vol, cls_id, m)

    print("  ✔  Subtomogram extraction complete.")
