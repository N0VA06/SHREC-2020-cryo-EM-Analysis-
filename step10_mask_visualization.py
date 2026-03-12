
import os
import matplotlib.pyplot as plt

from config import DATASET_ROOT, NUM_MODELS, FIGSIZE_WIDE, CMAP_GRAY
from utils  import load_mrc, save_fig, label_axes, add_colorbar


def run():
    for m in range(NUM_MODELS):
        base   = os.path.join(DATASET_ROOT, f"model_{m}")
        gm_p   = os.path.join(base, "grandmodel.mrc")
        mask_p = os.path.join(base, "class_mask.mrc")
        bbox_p = os.path.join(base, "class_bbox.mrc")

        if not os.path.isfile(gm_p):
            continue

        gm  = load_mrc(gm_p)
        z   = gm.shape[0] // 2
        raw = gm[z]

        # ── Class mask overlay ─────────────────────────────────────────────────
        if os.path.isfile(mask_p):
            mv   = load_mrc(mask_p)
            mz   = min(z, mv.shape[0] - 1)
            msl  = mv[mz] if mv.ndim >= 3 else mv

            fig, axes = plt.subplots(1, 3, figsize=FIGSIZE_WIDE)
            axes[0].imshow(raw, cmap=CMAP_GRAY, origin="lower")
            label_axes(axes[0], "Raw Slice")

            axes[1].imshow(msl, cmap="tab20", origin="lower")
            label_axes(axes[1], "Class Mask")

            axes[2].imshow(raw, cmap=CMAP_GRAY, origin="lower", alpha=0.7)
            im_ov = axes[2].imshow(msl, cmap="jet", origin="lower",
                                   alpha=0.4,
                                   vmin=msl.min(), vmax=msl.max())
            label_axes(axes[2], "Mask Overlay")
            add_colorbar(fig, axes[2], im_ov, "Class ID")

            fig.suptitle(f"model_{m} – Class Mask Overlay", fontweight="bold")
            save_fig(fig, "mask_visualization", "class_mask_overlay",
                     f"model_{m}_mask_overlay.png")

        # ── Bounding-box overlay ───────────────────────────────────────────────
        if os.path.isfile(bbox_p):
            bv  = load_mrc(bbox_p)
            bz  = min(z, bv.shape[0] - 1)
            bsl = bv[bz] if bv.ndim >= 3 else bv

            fig2, axes2 = plt.subplots(1, 3, figsize=FIGSIZE_WIDE)
            axes2[0].imshow(raw, cmap=CMAP_GRAY, origin="lower")
            label_axes(axes2[0], "Raw Slice")

            axes2[1].imshow(bsl, cmap="hot", origin="lower")
            label_axes(axes2[1], "BBox Volume")

            axes2[2].imshow(raw, cmap=CMAP_GRAY, origin="lower", alpha=0.7)
            im_bb = axes2[2].imshow(bsl, cmap="hot", origin="lower",
                                    alpha=0.4,
                                    vmin=bsl.min(), vmax=bsl.max())
            label_axes(axes2[2], "BBox Overlay")
            add_colorbar(fig2, axes2[2], im_bb, "BBox")

            fig2.suptitle(f"model_{m} – Bounding Box Overlay", fontweight="bold")
            save_fig(fig2, "mask_visualization", "bbox_overlay",
                     f"model_{m}_bbox_overlay.png")

    print("  ✔  Mask & bounding-box visualization complete.")
