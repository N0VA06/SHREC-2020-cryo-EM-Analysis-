import os
import numpy as np
import matplotlib.pyplot as plt

from config import DATASET_ROOT, NUM_MODELS, FIGSIZE_WIDE, CMAP_GRAY, CMAP_DIFF
from utils  import load_mrc, save_fig, label_axes, add_colorbar


def run():
    for m in range(NUM_MODELS):
        base  = os.path.join(DATASET_ROOT, f"model_{m}")
        gt_p  = os.path.join(base, "grandmodel.mrc")
        rec_p = os.path.join(base, "reconstruction.mrc")

        if not (os.path.isfile(gt_p) and os.path.isfile(rec_p)):
            continue

        gt  = load_mrc(gt_p)
        rec = load_mrc(rec_p)

        # Crop to shared extent if shapes differ
        zz = min(gt.shape[0], rec.shape[0])
        yy = min(gt.shape[1], rec.shape[1])
        xx = min(gt.shape[2], rec.shape[2])
        gt  = gt[:zz, :yy, :xx]
        rec = rec[:zz, :yy, :xx]

        z    = zz // 2
        diff = gt[z] - rec[z]

        # ── Slice comparison ──────────────────────────────────────────────────
        fig, axes = plt.subplots(1, 3, figsize=FIGSIZE_WIDE)
        for ax, data, title, cmap in zip(
            axes,
            [gt[z],   rec[z],          diff],
            ["Ground Truth Slice", "Reconstructed Slice", "Difference Map"],
            [CMAP_GRAY, CMAP_GRAY,     CMAP_DIFF],
        ):
            im = ax.imshow(data, cmap=cmap, origin="lower")
            label_axes(ax, title)
            add_colorbar(fig, ax, im)
        fig.suptitle(f"model_{m} – Reconstruction vs Ground Truth", fontweight="bold")
        save_fig(fig, "reconstruction_analysis", "reconstruction_vs_groundtruth",
                 f"model_{m}_comparison.png")

        # ── Slice variance along Z ────────────────────────────────────────────
        gt_var  = [gt[i].var()  for i in range(zz)]
        rec_var = [rec[i].var() for i in range(zz)]

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(gt_var,  label="Grand Model",    alpha=0.8)
        ax2.plot(rec_var, label="Reconstruction", alpha=0.8)
        ax2.set_xlabel("Z Slice Index")
        ax2.set_ylabel("Variance")
        ax2.set_title(f"model_{m} – Slice Variance along Z", fontweight="bold")
        ax2.legend()
        ax2.grid(True, linestyle="--", alpha=0.4)
        save_fig(fig2, "reconstruction_analysis", "slice_variance_plots",
                 f"model_{m}_variance_z.png")

        # ── Intensity histograms ──────────────────────────────────────────────
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        ax3.hist(gt.ravel(),  bins=200, alpha=0.55, label="Ground Truth",
                 color="royalblue",   density=True)
        ax3.hist(rec.ravel(), bins=200, alpha=0.55, label="Reconstruction",
                 color="darkorange",  density=True)
        ax3.set_xlabel("Intensity")
        ax3.set_ylabel("Density")
        ax3.set_title(f"model_{m} – Intensity Histograms: GT vs Reconstruction",
                      fontweight="bold")
        ax3.legend()
        save_fig(fig3, "reconstruction_analysis", "slice_variance_plots",
                 f"model_{m}_intensity_hist.png")

    print("  ✔  Reconstruction analysis complete.")
