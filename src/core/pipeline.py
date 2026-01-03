from pathlib import Path
import logging

from core.process import process_well
from core.types import PipelineResult

logger = logging.getLogger("clas")


def run_single_well(las_path: Path, cfg, output_dir: Path) -> PipelineResult:
    logger.info(f"Processing LAS: {las_path.name}")

    result = process_well(las_path, cfg)

    return PipelineResult(
        well=result["well"],
        df=result["df"],
        seams=result["seams"],
        seam_count=result["seam_count"],
        depth_min=result["depth_min"],
        depth_max=result["depth_max"],
        output_dir=output_dir,
    )