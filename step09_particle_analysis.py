
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from config import DATASET_ROOT, NUM_MODELS, PARTICLE_COLS
from utils  import save_fig, out


# ── I/O ───────────────────────────────────────────────────────────────────────

def _load(path: str) -> pd.DataFrame:
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


# ── Per-model plots ────────────────────────────────────────────────────────────

def _class_bar(df: pd.DataFrame, m: int):
    counts = df["class_id"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    counts.plot(kind="bar", ax=ax, color="steelblue", edgecolor="white")
    ax.set_title(f"model_{m} – Particle Count per Class", fontweight="bold")
    ax.set_xlabel("Class ID")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=45)
    save_fig(fig, "particle_analysis", "particle_histograms",
             f"model_{m}_class_counts.png")


def _scatter_2d(df: pd.DataFrame, m: int, cmap_cls: dict):
    classes = sorted(df["class_id"].unique())
    for x_col, y_col, plane in [("X", "Y", "XY"), ("X", "Z", "XZ")]:
        fig, ax = plt.subplots(figsize=(8, 6))
        for cls in classes:
            sub = df[df["class_id"] == cls]
            ax.scatter(sub[x_col], sub[y_col], s=10, alpha=0.6,
                       color=cmap_cls[cls], label=f"Class {int(cls)}")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"model_{m} – Particle Distribution ({plane})", fontweight="bold")
        ax.legend(markerscale=2, fontsize=7, ncol=2)
        save_fig(fig, "particle_analysis", "particle_3d_scatter",
                 f"model_{m}_scatter_{plane}.png")


def _scatter_3d(df: pd.DataFrame, m: int, cmap_cls: dict):
    classes = sorted(df["class_id"].unique())
    fig = plt.figure(figsize=(9, 7))
    ax  = fig.add_subplot(111, projection="3d")
    for cls in classes:
        sub = df[df["class_id"] == cls]
        ax.scatter(sub["X"], sub["Y"], sub["Z"], s=6, alpha=0.5,
                   color=cmap_cls[cls], label=f"Class {int(cls)}")
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.set_title(f"model_{m} – 3D Particle Distribution", fontweight="bold")
    ax.legend(markerscale=2, fontsize=7, ncol=2, loc="upper left")
    save_fig(fig, "particle_analysis", "particle_3d_scatter",
             f"model_{m}_scatter_3D.png", tight=False)


# ── Public entry point ────────────────────────────────────────────────────────

def run():
    all_dfs = []

    for m in range(NUM_MODELS):
        path = os.path.join(DATASET_ROOT, f"model_{m}", "particle_locations.txt")
        if not os.path.isfile(path):
            continue
        df = _load(path)
        df["model"] = m
        all_dfs.append(df)

        if df.empty:
            continue

        classes   = sorted(df["class_id"].unique())
        colors    = plt.cm.tab20(np.linspace(0, 1, len(classes)))
        cmap_cls  = {c: col for c, col in zip(classes, colors)}

        _class_bar(df, m)
        _scatter_2d(df, m, cmap_cls)
        _scatter_3d(df, m, cmap_cls)

    if not all_dfs:
        print("  ⚠  No particle_locations.txt files found.")
        return

    df_all = pd.concat(all_dfs, ignore_index=True)
    dest   = out("particle_analysis", "particle_distribution",
                 "all_particle_locations.csv")
    df_all.to_csv(dest, index=False)
    print(f"  ✔  Particle analysis complete. Combined CSV → {dest}")
