"""Helpers shared by the regression notebooks in this folder.

The notebooks follow the plotting conventions of *Hands-On Machine Learning with
Scikit-Learn, Keras & TensorFlow* (Géron), where `save_fig` saves the current figure as a
high-resolution PNG instead of repeating `plt.savefig(...)` boilerplate everywhere.

This module is part of the separate comparison experiment (Phase 8); the StudyGraph
application never imports it.
"""

from pathlib import Path

import matplotlib.pyplot as plt

IMAGES_PATH = Path(__file__).resolve().parent / "images"


def save_fig(fig_id: str, tight_layout: bool = True, fig_extension: str = "png", resolution: int = 300) -> Path:
    """Save the current matplotlib figure and return where it was written.

    Args:
        fig_id: File stem without extension, e.g. ``"scatter_matrix"``.
        tight_layout: Call ``plt.tight_layout()`` before saving.
        fig_extension: Image format, also used as the file extension.
        resolution: DPI of the saved image.
    """
    if not fig_id or not fig_id.strip():
        raise ValueError("fig_id must be a non-empty file name")
    IMAGES_PATH.mkdir(parents=True, exist_ok=True)
    path = IMAGES_PATH / f"{fig_id}.{fig_extension}"
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)
    return path
