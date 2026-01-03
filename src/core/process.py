from pathlib import Path
import pandas as pd

from core.io import read_las
from core.preprocessing import auto_trim, infer_depth_step
from core.scoring import compute_clas
from core.seams import extract_seams

def process_well(las_path: Path, cfg) -> dict:
    df, well = read_las(las_path)

    df = auto_trim(df)

    df["CLAS"] = compute_clas(df, cfg)

    # conservative coal decision
    coal_votes = (df["CLAS"] >= cfg.point_threshold).rolling(
        window=3,
        center=True,
        min_periods=1
    ).sum()

    df["IS_COAL"] = coal_votes >= 2

    seams = extract_seams(df, cfg)

    return {
        "well": well,
        "df": df,
        "seams": seams,
        "seam_count": len(seams),
        "depth_min": df["DEPT"].min(),
        "depth_max": df["DEPT"].max(),
    }