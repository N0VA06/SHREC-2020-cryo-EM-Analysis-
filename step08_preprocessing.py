import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from skimage import exposure

from config import DATASET_ROOT, NUM_MODELS, FIGSIZE_WIDE, CMAP_GRAY, CMAP_DIFF
from utils  import load_mrc, save_fig, label_axes, add_colorbar, norm01


# ── Internal helper ───────────────────────────────────────────────────────────

def _panel(original: np.ndarray,
           processed: np.ndarray,
           method_name: str,
           model_tag: int,
           subfolder: str):
    """Save a 3-panel (Original / Processed / Difference) figure."""
    diff = original - processed
    fig, axes = plt.subplots(1, 3, figsize=FIGSIZE_WIDE)
    for ax, data, title, cmap in zip(
        axes,
        [original,  processed,       diff],
        ["Original", f"Processed ({method_name})", "Difference Map"],
        [CMAP_GRAY, CMAP_GRAY,        CMAP_DIFF],
    ):
        im = ax.imshow(data, cmap=cmap, origin="lower")
        label_axes(ax, title)
        add_colorbar(fig, ax, im)
    fig.suptitle(f"model_{model_tag} – {method_name}", fontweight="bold")
    fname = f"model_{model_tag}_{method_name.lower().replace(' ', '_')}.png"
    save_fig(fig, "preprocessing", subfolder, fname)


# ── Public entry point ────────────────────────────────────────────────────────

def run():
    for m in range(NUM_MODELS):
        path = os.path.join(DATASET_ROOT, f"model_{m}", "grandmodel.mrc")
        if not os.path.isfile(path):
            continue

        vol = load_mrc(path)
        slc = vol[vol.shape[0] // 2].astype(np.float32)

        # ── Normalisation ──────────────────────────────────────────────────────
        minmax = norm01(slc)
        zscore = (slc - slc.mean()) / (slc.std() + 1e-8)
        _panel(slc, minmax, "Min-Max Normalization", m, "normalization")
        _panel(slc, zscore, "Z-Score Normalization", m, "normalization")

        # ── Denoising ──────────────────────────────────────────────────────────
        gauss  = ndi.gaussian_filter(slc, sigma=1.5)
        median = ndi.median_filter(slc, size=3)
        _panel(slc, gauss,  "Gaussian Denoising", m, "denoising")
        _panel(slc, median, "Median Denoising",   m, "denoising")

        # ── Contrast enhancement ───────────────────────────────────────────────
        slc_u8 = exposure.rescale_intensity(slc, out_range=np.uint8)
        he     = exposure.equalize_hist(slc_u8).astype(np.float32) * 255
        clahe  = (exposure.equalize_adapthist(slc_u8 / 255.0, clip_limit=0.03)
                  .astype(np.float32) * 255)
        _panel(slc, he,    "Histogram Equalization", m, "contrast_enhancement")
        _panel(slc, clahe, "CLAHE",                  m, "contrast_enhancement")

    print("  ✔  Preprocessing visualizations complete.")
