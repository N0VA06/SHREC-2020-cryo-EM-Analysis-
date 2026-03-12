
from utils import mkdirs, out


def run():
    dirs = [
        out("dataset_summary"),
        out("slice_visualizations", "grandmodel"),
        out("slice_visualizations", "reconstruction"),
        out("slice_visualizations", "noisefree"),
        out("noise_analysis", "before_after_noise"),
        out("noise_analysis", "noise_histograms"),
        out("projection_analysis", "tilt_series_visualization"),
        out("projection_analysis", "before_after_projection"),
        out("reconstruction_analysis", "reconstruction_vs_groundtruth"),
        out("reconstruction_analysis", "slice_variance_plots"),
        out("preprocessing", "normalization"),
        out("preprocessing", "denoising"),
        out("preprocessing", "contrast_enhancement"),
        out("particle_analysis", "particle_distribution"),
        out("particle_analysis", "particle_histograms"),
        out("particle_analysis", "particle_3d_scatter"),
        out("mask_visualization", "class_mask_overlay"),
        out("mask_visualization", "bbox_overlay"),
        out("subtomograms", "extracted_particles"),
        out("subtomograms", "subtomogram_examples"),
        out("figures_summary", "comparison_panels"),
    ]
    mkdirs(*dirs)
    print("  ✔  Output directories created.")
