import os
import numpy as np
import matplotlib.pyplot as plt

from config import DATASET_ROOT, NUM_MODELS, CMAP_GRAY
from utils  import load_mrc, save_fig, label_axes, add_colorbar, out


def _plot_plane(vol: np.ndarray, title_prefix: str, save_folder: str, tag: str):
    """Generate central + random slice figures for XY, XZ, YZ planes."""
    z, y, x = vol.shape
    np.random.seed(42)

    planes = {
        "XY": (vol[z // 2],          vol[np.random.randint(0, z)]),
        "XZ": (vol[:, y // 2, :],    vol[:, np.random.randint(0, y), :]),
        "YZ": (vol[:, :, x // 2],    vol[:, :, np.random.randint(0, x)]),
    }

    for plane, (central, rand_sl) in planes.items():
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        for ax, slc, lbl in zip(
            axes,
            [central, rand_sl],
            ["Central Slice", "Random Slice"],
        ):
            im = ax.imshow(slc, cmap=CMAP_GRAY, origin="lower")
            label_axes(ax, f"{title_prefix} – {plane} {lbl}")
            add_colorbar(fig, ax, im)

        fname = f"{tag}_{plane}.png"
        save_fig(fig, save_folder, fname)


def run():
    targets = [
        ("grandmodel.mrc",           os.path.join("slice_visualizations", "grandmodel")),
        ("reconstruction.mrc",       os.path.join("slice_visualizations", "reconstruction")),
        ("grandmodel_noisefree.mrc", os.path.join("slice_visualizations", "noisefree")),
    ]

    for m in range(NUM_MODELS):
        base = os.path.join(DATASET_ROOT, f"model_{m}")

        for vfile, folder in targets:
            path = os.path.join(base, vfile)
            if not os.path.isfile(path):
                continue
            vol = load_mrc(path)
            if vol.ndim < 3:
                continue
            _plot_plane(vol, f"model_{m}/{vfile}", folder, f"model_{m}")

    print("  ✔  Slice visualizations complete.")
