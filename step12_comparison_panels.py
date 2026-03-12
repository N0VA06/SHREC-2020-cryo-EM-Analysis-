
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from skimage import exposure

from config import DATASET_ROOT, NUM_MODELS, CMAP_GRAY
from utils  import load_mrc, save_fig, label_axes, add_colorbar, norm01


def run():
    for m in range(NUM_MODELS):
        path = os.path.join(DATASET_ROOT, f"model_{m}", "grandmodel.mrc")
        if not os.path.isfile(path):
            continue

        vol = load_mrc(path)
        slc = vol[vol.shape[0] // 2].astype(np.float32)

        # Build the four variants
        minmax = norm01(slc)
        gauss  = ndi.gaussian_filter(slc, sigma=1.5)
        slc_u8 = exposure.rescale_intensity(slc, out_range=np.uint8)
        clahe  = (exposure.equalize_adapthist(slc_u8 / 255.0, clip_limit=0.03)
                  .astype(np.float32) * 255)

        panels = [
            (slc,    "Original"),
            (minmax, "Normalized (Min-Max)"),
            (gauss,  "Denoised (Gaussian)"),
            (clahe,  "Contrast (CLAHE)"),
        ]

        fig, axes = plt.subplots(1, 4, figsize=(22, 5))
        for ax, (img, title) in zip(axes, panels):
            im = ax.imshow(img, cmap=CMAP_GRAY, origin="lower")
            label_axes(ax, title)
            add_colorbar(fig, ax, im)

        fig.suptitle(
            f"model_{m} – Preprocessing Comparison Panel",
            fontsize=14,
            fontweight="bold",
        )
        save_fig(fig, "figures_summary", "comparison_panels",
                 f"model_{m}_panel.png")

    print("  ✔  Final comparison panels complete.")
