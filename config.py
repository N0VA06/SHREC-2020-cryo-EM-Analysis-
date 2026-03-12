"""
config.py
─────────
Central configuration for the SHREC 2020 Cryo-ET analysis pipeline.
Edit DATASET_ROOT / OUTPUT_ROOT to match your environment.
"""

import os

# ── Paths ────────────────────────────────────────────────────────────────────
DATASET_ROOT = os.path.expanduser("/home/nova/shrec/shrec2020_full_dataset")
OUTPUT_ROOT  = os.path.expanduser("/home/nova/Videos/files/results")

# ── Dataset layout ───────────────────────────────────────────────────────────
NUM_MODELS = 10          # model_0 … model_9

VOLUME_FILES = [
    "grandmodel.mrc",
    "grandmodel_noisefree.mrc",
    "class_bbox.mrc",
    "class_mask.mrc",
    "occupancy_bbox.mrc",
    "occupancy_mask.mrc",
    "projections.mrc",
    "projections_noisefree.mrc",
    "reconstruction.mrc",
]
OTHER_FILES = ["particle_locations.txt"]
ALL_FILES   = VOLUME_FILES + OTHER_FILES

PARTICLE_COLS = ["class_id", "X", "Y", "Z", "rot_Z1", "rot_X", "rot_Z2"]

# ── Subtomogram ───────────────────────────────────────────────────────────────
CUBE_SIZE = 32

# ── Plot style ────────────────────────────────────────────────────────────────
DPI          = 300
FIGSIZE_WIDE = (18, 5)
FIGSIZE_SQ   = (14, 14)
CMAP_GRAY    = "gray"
CMAP_DIFF    = "RdBu_r"
CMAP_HEAT    = "hot"
