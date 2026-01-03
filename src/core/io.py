import lasio
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

def read_las(path: Path):
    las = lasio.read(str(path))

    well_name = (
        str(las.well.WELL.value).strip()
        if "WELL" in las.well
        else path.stem
    )

    logger.info(f"Reading LAS: {path.name}")
    
    df = las.df().reset_index()
    df.columns = df.columns.str.upper()
    df = df.replace(-999, np.nan)

    col_variants: Dict[str, List[str]] = {
        "DEPT": ["DEPT", "DEPTH", "MD"],
        "GR": ["GR", "GAPI", "GR_CPS"],
        "LD": ["LD", "LDT", "LDS"],
        "SD": ["SD", "RHOB"],
        "CL": ["CL", "CAL", "CALI", "CALIPER"]
    }

    rename = {}
    for std, opts in col_variants.items():
        for o in opts:
            if o in df.columns:
                rename[o] = std
                break

    df = df.rename(columns=rename)
    df = df.sort_values("DEPT").reset_index(drop=True)

    if "DEPT" not in df.columns:
        raise ValueError("Depth column not found in LAS file")

    return df, well_name