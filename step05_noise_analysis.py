import os
import numpy as np
import matplotlib.pyplot as plt

from config import DATASET_ROOT, NUM_MODELS, FIGSIZE_WIDE, CMAP_GRAY, CMAP_DIFF
from utils  import load_mrc, save_fig, label_axes, add_colorbar, snr_db


def run():
    for m in range(NUM_MODELS):
        base        = os.path.join(DATASET_ROOT, f"model_{m}")
        noisy_path  = os.path.join(base, "grandmodel.mrc")
        clean_path  = os.path.join(base, "grandmodel_noisefree.mrc")

        if not (os.path.isfile(noisy_path) and os.path.isfile(clean_path)):
            continue

        noisy = load_mrc(noisy_path)
        clean = load_mrc(clean_path)

        z        = noisy.shape[0] // 2
        noisy_sl = noisy[z]
        clean_sl = clean[z]
        diff_sl  = noisy_sl - clean_sl

        # ── Before / After / Difference ───────────────────────────────────────
        fig, axes = plt.subplots(1, 3, figsize=FIGSIZE_WIDE)
        for ax, data, title, cmap in zip(
            axes,
            [noisy_sl,  clean_sl,    diff_sl],
            ["Noisy Slice", "Noise-Free Slice", "Noise Difference Map"],
            [CMAP_GRAY, CMAP_GRAY,   CMAP_DIFF],
        ):
            im = ax.imshow(data, cmap=cmap, origin="lower")
            label_axes(ax, title)
            add_colorbar(fig, ax, im)
        fig.suptitle(f"model_{m} – Noise Analysis", fontsize=13, fontweight="bold")
        save_fig(fig, "noise_analysis", "before_after_noise",
                 f"model_{m}_before_after.png")

        # ── Intensity histograms ──────────────────────────────────────────────
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.hist(noisy.ravel(), bins=200, alpha=0.6, label="Noisy",
                 color="steelblue", density=True)
        ax2.hist(clean.ravel(), bins=200, alpha=0.6, label="Noise-Free",
                 color="tomato", density=True)
        ax2.set_title(f"model_{m} – Intensity Histograms", fontweight="bold")
        ax2.set_xlabel("Intensity")
        ax2.set_ylabel("Density")
        ax2.legend()
        save_fig(fig2, "noise_analysis", "noise_histograms",
                 f"model_{m}_histograms.png")

        # ── SNR bar chart ─────────────────────────────────────────────────────
        snr = snr_db(clean_sl, diff_sl)
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        bar = ax3.bar(["SNR (dB)"], [snr], color="seagreen")
        ax3.bar_label(bar, fmt="%.2f dB")
        ax3.set_title(f"model_{m} – Signal-to-Noise Ratio", fontweight="bold")
        ax3.set_ylabel("dB")
        save_fig(fig3, "noise_analysis", "noise_histograms",
                 f"model_{m}_snr.png")

    print("  ✔  Noise analysis complete.")
