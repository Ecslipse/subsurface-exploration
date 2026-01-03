from pathlib import Path
import pandas as pd
from typing import Literal

from viz.plotlib_qc import plot_qc as plot_qc_matplotlib

PlotBackend = Literal["matplotlib"]

def plot_qc(
    *,
    df: pd.DataFrame,
    seams: pd.DataFrame,
    well_name: str,
    out_dir: Path,
    threshold: float,
    plot: bool,
    save: bool,
    backend: PlotBackend = "matplotlib",
) -> None:
    if backend == "matplotlib":
        plot_qc_matplotlib(
            df=df,
            seams=seams,
            well_name=well_name,
            out_dir=out_dir,
            threshold=threshold,
            plot=plot,
            save=save,
        )
    else:
        raise ValueError(f"Unsupported plot backend: {backend}")