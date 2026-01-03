import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

DEPTH_STEP = 0.02

def robust_normalize(series, pmin=5, pmax=95):
    if series.dropna().empty:
        return pd.Series(np.nan, index=series.index)

    lo, hi = np.nanpercentile(series, [pmin, pmax])
    if hi <= lo:
        return pd.Series(np.nan, index=series.index)

    return ((series - lo) / (hi - lo)).clip(0, 1)

# Because the current data contain inconsistent data, we trim it to make the calculation easier
def auto_trim(df: pd.DataFrame) -> pd.DataFrame:
    depth = df["DEPT"]

    depth = depth[depth.notna()]
    df = df.loc[depth.index]

    return df.reset_index(drop=True)

def infer_depth_step(df):
    d = np.diff(df["DEPT"].astype(float))
    d = d[(d > 0) & ~np.isnan(d)]
    return float(np.median(d)) if len(d) else DEPTH_STEP

def neighbor_context(series, window):
    return series.rolling(
        window=window,
        center=True,
        min_periods=1
    ).mean()