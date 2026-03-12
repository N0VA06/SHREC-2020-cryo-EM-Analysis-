"""
main.py
───────
SHREC 2020 Cryo-ET Full Analysis Pipeline — Orchestrator

Usage
─────
    conda activate monai_env
    python main.py [--steps 1 2 3 ...]   # run specific steps only
    python main.py                        # run all steps

Steps
─────
  1  Create output directories
  2  Dataset structure analysis
  3  Volume statistics
  4  Slice visualizations
  5  Noise analysis (before / after)
  6  Projection analysis
  7  Reconstruction analysis
  8  Preprocessing visualizations
  9  Particle location analysis
 10  Mask & bounding-box visualization
 11  Subtomogram extraction
 12  Final comparison panels
"""

import argparse
import sys
import textwrap
import traceback
import time
from typing import List

# ── Step modules ──────────────────────────────────────────────────────────────
import step01_create_dirs
import step02_dataset_structure
import step03_volume_statistics
import step04_slice_visualizations
import step05_noise_analysis
import step06_projection_analysis
import step07_reconstruction_analysis
import step08_preprocessing
import step09_particle_analysis
import step10_mask_visualization
import step11_subtomogram_extraction
import step12_comparison_panels

from config import DATASET_ROOT, OUTPUT_ROOT

# ── Step registry ─────────────────────────────────────────────────────────────
STEPS = [
    (1,  "Create output directories",          step01_create_dirs),
    (2,  "Dataset structure analysis",          step02_dataset_structure),
    (3,  "Volume statistics",                   step03_volume_statistics),
    (4,  "Slice visualizations",                step04_slice_visualizations),
    (5,  "Noise analysis (before / after)",     step05_noise_analysis),
    (6,  "Projection analysis",                 step06_projection_analysis),
    (7,  "Reconstruction analysis",             step07_reconstruction_analysis),
    (8,  "Preprocessing visualizations",        step08_preprocessing),
    (9,  "Particle location analysis",          step09_particle_analysis),
    (10, "Mask & bounding-box visualization",   step10_mask_visualization),
    (11, "Subtomogram extraction",              step11_subtomogram_extraction),
    (12, "Final comparison panels",             step12_comparison_panels),
]


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SHREC 2020 Cryo-ET Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python main.py                   # run all 12 steps
              python main.py --steps 1 2 3     # run only steps 1, 2, 3
              python main.py --steps 5 6 7     # run noise + projection + recon
        """),
    )
    parser.add_argument(
        "--steps",
        nargs="+",
        type=int,
        metavar="N",
        help="Step numbers to run (default: all)",
    )
    return parser.parse_args()


# ── Runner ────────────────────────────────────────────────────────────────────

def _divider(char: str = "─", width: int = 62) -> str:
    return char * width


def run_pipeline(step_numbers: List[int]):
    selected = (
        [(n, name, mod) for n, name, mod in STEPS if n in step_numbers]
        if step_numbers
        else STEPS
    )

    if not selected:
        print("No matching steps found. Exiting.")
        sys.exit(1)

    print(_divider("═"))
    print("  SHREC 2020 Cryo-ET — Analysis Pipeline")
    print(f"  Dataset : {DATASET_ROOT}")
    print(f"  Output  : {OUTPUT_ROOT}")
    print(_divider("═"))
    print(f"  Running {len(selected)} / {len(STEPS)} step(s)\n")

    results = {}        # step_number -> "ok" | "failed"
    t_total = time.time()

    for n, name, mod in selected:
        prefix = f"[{n:02d}/{len(STEPS):02d}]"
        print(f"{prefix} {name} …")
        t0 = time.time()
        try:
            mod.run()
            elapsed = time.time() - t0
            print(f"         └─ done in {elapsed:.1f}s")
            results[n] = "ok"
        except Exception:
            elapsed = time.time() - t0
            print(f"         └─ ⚠  FAILED after {elapsed:.1f}s")
            print(textwrap.indent(traceback.format_exc(), "         "))
            results[n] = "failed"

    # ── Summary ───────────────────────────────────────────────────────────────
    elapsed_total = time.time() - t_total
    ok     = sum(1 for v in results.values() if v == "ok")
    failed = sum(1 for v in results.values() if v == "failed")

    print()
    print(_divider())
    print(f"  Pipeline finished in {elapsed_total:.1f}s")
    print(f"  Steps passed : {ok}")
    if failed:
        print(f"  Steps failed : {failed}")
        for n, status in results.items():
            if status == "failed":
                name = next(nm for num, nm, _ in STEPS if num == n)
                print(f"    • Step {n:02d}: {name}")
    print(f"  Results saved → {OUTPUT_ROOT}")
    print(_divider("═"))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args.steps or [])
