from dataclasses import dataclass
from pathlib import Path
import pandas as pd

@dataclass(frozen=True)
class PipelineResult:
    well: str
    df: pd.DataFrame
    seams: pd.DataFrame
    seam_count: int
    depth_min: float
    depth_max: float
    output_dir: Path