import pandas as pd
from core.config import CLASConfig
from core.preprocessing import infer_depth_step
import logging

logger = logging.getLogger(__name__)
def extract_seams(df: pd.DataFrame, cfg: CLASConfig):
    step = infer_depth_step(df)
    seams = []

    in_zone = False
    gap = 0.0
    start = None

    for i in range(len(df)):
        is_coal = bool(df.loc[i, "IS_COAL"])
        clas = df.loc[i, "CLAS"]

        if is_coal and not in_zone:
            start = df.loc[i, "DEPT"]
            in_zone = True
            gap = 0.0

        elif in_zone:
            if not is_coal:
                if pd.isna(clas):
                    gap += step
                else:
                    gap += step * 2  

                if gap > cfg.max_no_data_run:
                    end = df.loc[i - 1, "DEPT"]
                    thick = end - start + step # type: ignore

                    if thick >= cfg.min_thickness: # type: ignore
                        seg = df[(df["DEPT"] >= start) & (df["DEPT"] <= end)]

                        valid = seg["CLAS"].notna()
                        if valid.any():
                            coal_conf = (
                                seg.loc[valid, "CLAS"] >= cfg.point_threshold
                            ).mean()
                        else:
                            coal_conf = float("nan")

                        seams.append({
                            "TOP": start,
                            "BOTTOM": end,
                            "THICKNESS": thick,
                            "MEAN_CLAS": seg["CLAS"].mean(),
                            "MIN_CLAS": seg["CLAS"].min(),
                            "COAL_CONF": coal_conf
                        })

                    in_zone = False

            else:
                gap = 0.0

    return pd.DataFrame(seams)