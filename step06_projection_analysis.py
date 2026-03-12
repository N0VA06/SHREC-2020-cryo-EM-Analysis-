

import os
import numpy as np
import matplotlib.pyplot as plt

from config import DATASET_ROOT, NUM_MODELS, FIGSIZE_WIDE, CMAP_GRAY, CMAP_DIFF
from utils  import load_mrc, save_fig, label_axes, add_colorbar


def run():
    for m in range(NUM_MODELS):
        base       = os.path.join(DATASET_ROOT, f"model_{m}")
        noisy_path = os.path.join(base, "projections.mrc")
        clean_path = os.path.join(base, "projections_noisefree.mrc")

        if not (os.path.isfile(noisy_path) and os.path.isfile(clean_path)):
            continue

        proj_noisy = load_mrc(noisy_path)
        proj_clean = load_mrc(clean_path)

        n_tilts     = proj_noisy.shape[0]
        tilt_angles = np.linspace(-60, 60, n_tilts)

        # ── Tilt-series strip ─────────────────────────────────────────────────
        step  = max(1, n_tilts // 9)
        idx   = list(range(0, n_tilts, step))[:9]
        ncols = len(idx)

        fig, axes = plt.subplots(1, ncols, figsize=(ncols * 2 + 1, 3))
        if ncols == 1:
            axes = [axes]
        for ax, i in zip(axes, idx):
            ax.imshow(proj_clean[i], cmap=CMAP_GRAY, origin="lower", aspect="auto")
            ax.set_title(f"{tilt_angles[i]:.0f}°", fontsize=8)
            ax.axis("off")
        fig.suptitle(f"model_{m} – Tilt Series (noise-free)", fontweight="bold")
        save_fig(fig, "projection_analysis", "tilt_series_visualization",
                 f"model_{m}_tilt_series.png")

        # ── Before / After at middle tilt ─────────────────────────────────────
        mid  = n_tilts // 2
        diff = proj_noisy[mid] - proj_clean[mid]

        fig2, axes2 = plt.subplots(1, 3, figsize=FIGSIZE_WIDE)
        for ax, data, title, cmap in zip(
            axes2,
            [proj_clean[mid], proj_noisy[mid], diff],
            ["Clean Projection", "Microscope Projection", "Difference Map"],
            [CMAP_GRAY, CMAP_GRAY, CMAP_DIFF],
        ):
            im = ax.imshow(data, cmap=cmap, origin="lower", aspect="auto")
            label_axes(ax, title)
            add_colorbar(fig2, ax, im)
        fig2.suptitle(
            f"model_{m} – Before/After Projection (tilt {tilt_angles[mid]:.0f}°)",
            fontweight="bold",
        )
        save_fig(fig2, "projection_analysis", "before_after_projection",
                 f"model_{m}_before_after.png")

        # ── Tilt angle vs projection index ────────────────────────────────────
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        ax3.plot(range(n_tilts), tilt_angles, "o-", color="steelblue")
        ax3.set_xlabel("Projection Index")
        ax3.set_ylabel("Tilt Angle (°)")
        ax3.set_title(f"model_{m} – Tilt Angle vs Projection Index", fontweight="bold")
        ax3.grid(True, linestyle="--", alpha=0.5)
        save_fig(fig3, "projection_analysis", "tilt_series_visualization",
                 f"model_{m}_tilt_angles.png")

        # ── Projection variance vs tilt angle ─────────────────────────────────
        variances = [proj_noisy[i].var() for i in range(n_tilts)]
        fig4, ax4 = plt.subplots(figsize=(8, 4))
        ax4.plot(tilt_angles, variances, "s-", color="tomato")
        ax4.set_xlabel("Tilt Angle (°)")
        ax4.set_ylabel("Projection Variance")
        ax4.set_title(f"model_{m} – Projection Variance vs Tilt Angle", fontweight="bold")
        ax4.grid(True, linestyle="--", alpha=0.5)
        save_fig(fig4, "projection_analysis", "tilt_series_visualization",
                 f"model_{m}_variance_vs_tilt.png")

    print("  ✔  Projection analysis complete.")
