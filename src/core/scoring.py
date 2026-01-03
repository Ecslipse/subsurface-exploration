import pandas as pd
import numpy as np
from core.preprocessing import robust_normalize, neighbor_context
from core.config import CLASConfig

def score_gr(gr_n):
    return (1.0 - gr_n / 0.6).clip(0, 1)

def score_density(dens_n):
    return ((dens_n - 0.6) / 0.4).clip(0, 1)

def score_stability(gr, window=5):
    std = gr.rolling(window, center=True, min_periods=2).std()
    ref = std.median()

    if ref == 0 or np.isnan(ref):
        return pd.Series(0.0, index=gr.index)

    return (1.0 - std / (2 * ref)).clip(0, 1)

def score_caliper(cal):
    return (1.0 - robust_normalize(cal)).clip(0, 1)

def score_data_quality(df):
    n_valid = df[["GR","LD","SD","CL"]].notna().sum(axis=1)
    return (n_valid / 4.0).clip(0, 1)

def compute_clas(df: pd.DataFrame, cfg: CLASConfig) -> pd.Series:
    df = df.copy()

    gr_n = robust_normalize(df["GR"])
    dens_n = robust_normalize(df[["LD","SD"]].median(axis=1))
    cal = df["CL"] if "CL" in df else pd.Series(np.nan, index=df.index)

    s_gr   = score_gr(gr_n)
    s_dens = score_density(dens_n)
    s_stab = score_stability(df["GR"])
    s_cal  = score_caliper(cal)

    s_gr   = neighbor_context(s_gr,   cfg.neighbor_window)
    s_dens = neighbor_context(s_dens, cfg.neighbor_window)
    s_cal  = neighbor_context(s_cal,  cfg.neighbor_window)

    score_sum = (
        cfg.w_gr   * s_gr +
        cfg.w_dens * s_dens +
        cfg.w_stab * s_stab +
        cfg.w_cal  * s_cal
    )

    weight_sum = (
        cfg.w_gr   * df["GR"].notna().astype(int) +
        cfg.w_dens * df[["LD","SD"]].notna().any(axis=1).astype(int) +
        cfg.w_stab * df["GR"].notna().astype(int) +
        cfg.w_cal  * df["CL"].notna().astype(int)
    )

    max_weight = cfg.w_gr + cfg.w_dens + cfg.w_stab + cfg.w_cal
    effective_weight = weight_sum / max_weight

    raw_clas = score_sum / weight_sum.replace(0, np.nan)

    q = score_data_quality(df)
    clas = raw_clas * q

    votes = (
        (s_gr > 0.6).astype(int) +
        (s_dens > 0.6).astype(int) +
        (s_cal > 0.6).astype(int)
    )

    clas = clas * (votes >= 2)

    clas[effective_weight < cfg.min_effective_weight] = np.nan

    return clas.clip(0, 1)