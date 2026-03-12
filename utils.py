"""
utils.py
────────
Shared helper utilities used across all pipeline steps.
"""

import os
import warnings
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mrcfile

from config import OUTPUT_ROOT, DPI

warnings.filterwarnings("ignore")


# ── Directory helpers ─────────────────────────────────────────────────────────

def mkdirs(*paths):
    """Create directories (and parents) silently."""
    for p in paths:
        os.makedirs(p, exist_ok=True)


def out(*parts):
    """Build an absolute output path under OUTPUT_ROOT."""
    return os.path.join(OUTPUT_ROOT, *parts)


# ── MRC I/O ───────────────────────────────────────────────────────────────────

def load_mrc(path: str) -> np.ndarray:
    """Return float32 data array from an MRC file (read-only, permissive)."""
    with mrcfile.open(path, mode="r", permissive=True) as mrc:
        return mrc.data.copy().astype(np.float32)


# ── Numeric helpers ───────────────────────────────────────────────────────────

def norm01(arr: np.ndarray) -> np.ndarray:
    """Min-max normalise to [0, 1]."""
    lo, hi = arr.min(), arr.max()
    if hi == lo:
        return np.zeros_like(arr)
    return (arr - lo) / (hi - lo)


def snr_db(signal: np.ndarray, noise: np.ndarray) -> float:
    """Estimate SNR in decibels: 20·log10(σ_signal / σ_noise)."""
    s, n = signal.std(), noise.std()
    if n == 0:
        return float("inf")
    return 20.0 * np.log10(s / n)


def central_slices(vol: np.ndarray):
    """Return (xy_slice, xz_slice, yz_slice) at volume centre."""
    z, y, x = vol.shape
    return vol[z // 2], vol[:, y // 2, :], vol[:, :, x // 2]


# ── Matplotlib helpers ────────────────────────────────────────────────────────

def save_fig(fig, *path_parts, tight: bool = True):
    """Save a matplotlib figure into OUTPUT_ROOT / *path_parts at DPI."""
    path = out(*path_parts)
    if tight:
        fig.tight_layout()
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def label_axes(ax, title: str, xlabel: str = "X", ylabel: str = "Y"):
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)


def add_colorbar(fig, ax, im, label: str = "Intensity"):
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(label, fontsize=7)
    return cb
