from dataclasses import dataclass, replace
from pathlib import Path
import yaml
from typing import Any, Dict

@dataclass(frozen=True)
class CLASConfig:
    min_thickness: float = 1.0
    point_threshold: float = 0.55
    min_effective_weight: float = 0.3

    w_gr: float = 0.4
    w_dens: float = 0.35
    w_stab: float = 0.15
    w_cal: float = 0.1

    neighbor_window: int = 5
    max_no_data_run: float = 1.0

    @classmethod
    def from_yaml(cls, path: Path) -> "CLASConfig":
        base = cls()

        with path.open("r") as f:
            raw: Dict[str, Any] = yaml.safe_load(f) or {}

        weights = raw.get("weights", {})
        thresholds = raw.get("thresholds", {})

        return replace(
            base,
            w_gr=weights.get("gamma_ray", base.w_gr),
            w_dens=weights.get("density", base.w_dens),
            w_cal=weights.get("caliper", base.w_cal),
            w_stab=weights.get("stability", base.w_stab),
            point_threshold=thresholds.get("point_threshold", base.point_threshold),
            min_thickness=thresholds.get("min_thickness", base.min_thickness),
        )