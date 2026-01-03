import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from pathlib import Path
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Flexible seam naming for large well interpretation
def seam_label(index: int) -> str:
    """0 -> A, 25 -> Z, 26 -> AA"""
    label = ""
    while True:
        index, rem = divmod(index, 26)
        label = chr(65 + rem) + label
        if index == 0:
            break
        index -= 1
    return label

def plot_qc(
    df: pd.DataFrame,
    seams: pd.DataFrame,
    well_name: str,
    out_dir: Path,
    threshold: float = 0.7,
    plot: bool = True,
    save: bool = True,
) -> Figure:

    fig, axes = plt.subplots(
        1, 4,
        figsize=(13, 10),
        sharey=True,
        width_ratios=[1, 1, 1, 0.9]
    )

    ax_gr, ax_dens, ax_clas, ax_info = axes

    # -------------------------
    # GR TRACK
    # -------------------------
    ax_gr.plot(df["GR"], df["DEPT"], color="darkgreen", linewidth=0.8)
    ax_gr.set_xlabel("GR")
    ax_gr.set_ylabel("Depth (m)")
    ax_gr.invert_yaxis()
    ax_gr.grid(True, linestyle="--", alpha=0.5)

    # -------------------------
    # DENSITY TRACK
    # -------------------------
    dens_cols = [c for c in ("LD", "SD") if c in df.columns]
    if dens_cols:
        dens = df[dens_cols].median(axis=1, skipna=True)
        valid = dens.notna()
        if valid.any():
            ax_dens.plot(
                dens[valid],
                df.loc[valid, "DEPT"],
                color="navy",
                linewidth=0.8
            )

    else:
        ax_dens.text(
            0.5, 0.5,
            "Density log\nnot available",
            ha="center", va="center",
            transform=ax_dens.transAxes
        )

    ax_dens.grid(True, linestyle="--", alpha=0.5)

    # -------------------------
    # C-LAS TRACK
    # -------------------------
    mask_pos = df["CLAS"].notna() & (df["CLAS"] > 0)

    sc = ax_clas.scatter(
        df.loc[mask_pos, "CLAS"],
        df.loc[mask_pos, "DEPT"],
        c=df.loc[mask_pos, "CLAS"],
        cmap="viridis",
        s=8
    )

    ax_clas.axvline(threshold, color="red", linestyle="--", linewidth=1)
    ax_clas.set_xlabel("CCI")
    ax_clas.grid(True, linestyle="--", alpha=0.5)
    plt.colorbar(sc, ax=ax_clas)

    # -------------------------
    # COAL SHADING
    # -------------------------
    for _, seam in seams.iterrows():
        for ax in (ax_gr, ax_dens, ax_clas):
            ax.axhspan(
                seam["TOP"],
                seam["BOTTOM"],
                color="black",
                alpha=0.25
            )

    # -------------------------
    # INFO PANEL
    # -------------------------
    ax_info.axis("off")

    ax_info.axis("off")

    if seams.empty:
        seam_summary = "No coal seams detected."
    else:
        lines = []
        for i, seam in seams.iterrows():
            label = seam_label(i) # type: ignore
            conf = seam.get("COAL_CONF", np.nan)
            conf_txt = "N/A" if np.isnan(conf) else f"{conf*100:.0f}%"

            lines.append(
                f"Seam {label}:\n"
                f"  {seam['TOP']:.2f} – {seam['BOTTOM']:.2f} m\n"
                f"  Thickness : {seam['THICKNESS']:.2f} m\n"
                f"  Coal Conf : {conf_txt}\n"
                f"  Mean CCI  : {seam['MEAN_CLAS']:.2f}\n"
            )

        seam_summary = "\n".join(lines)

    info_text = (
        f"WELL: {well_name}\n"
        "====================\n\n"
        "INTERPRETATION GUIDE\n"
        "--------------------\n"
        "CCI Score (color):\n"
        "Coal confidence Index score\n\n"
        "Shaded intervals:\n"
        "Detected coal seams\n\n"
        "Threshold:\n"
        "≥ 0.55  Likely coal\n\n"
        "SEAM SUMMARY\n"
        "--------------------\n"
        f"{seam_summary}"
    )

    ax_info.text(0.0, 0.95, info_text, fontsize=10, va="top")

    # -------------------------
    # SAVE
    # -------------------------
    out_path = out_dir / f"{well_name} C-LAS QC.png"
    fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.05, wspace=0.25)

    if save:
        out_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=200)
        logger.info(f"Saved QC plot → {out_path.resolve()}")
        
    if plot:
        plt.show(block=True)

    return fig