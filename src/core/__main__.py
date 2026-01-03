from pathlib import Path
from time import perf_counter
import pandas as pd
import logging

from core.cli import parse_args, setup_logging
from core.pipeline import run_single_well
from viz.plot_config import plot_qc
from core.config import CLASConfig
    
def main() -> None:
    args = parse_args()
    setup_logging(args.verbose, args.quiet)

    logger = logging.getLogger("clas")

    # Resolve LAS paths
    if args.las:
        las_files = [Path(p).resolve() for p in args.las]
    else:
        las_files = sorted(Path(args.las_dir).glob("*.las"))

    if not las_files:
        raise SystemExit("No LAS files found")

    output_root = Path(args.output).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    logger.info("C-LAS started")

    logger.info(f"Found {len(las_files)} LAS file(s)")

    if args.config:
        cfg = CLASConfig.from_yaml(args.config)
        logger.info(f"Loaded config from {args.config}")

    else:
        cfg = CLASConfig()
        logger.info("Using default CLAS configuration")
        
    logger.info(f"CLASConfig: {cfg}")

    for las_path in las_files:
        start = perf_counter()

        well_out = output_root / las_path.stem
        well_out.mkdir(parents=True, exist_ok=True)

        result = run_single_well(
            las_path=las_path,
            cfg=cfg,
            output_dir=well_out,
        )
        if args.plot or args.save_plot:
            plot_qc(
                df=result.df,
                seams=result.seams,
                well_name=result.well,
                out_dir=result.output_dir,
                threshold=cfg.point_threshold,
                plot=args.plot,
                save=args.save_plot,
                backend="matplotlib",
            )

        elapsed = perf_counter() - start

        logger.info("✔ Processing complete")
        logger.info(f"✔ Well: {result.well}")
        logger.info(f"✔ Coal seams detected: {result.seam_count}")
        logger.info(f"✔ Output directory: {result.output_dir}")
        logger.info(f"✔ Elapsed time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
