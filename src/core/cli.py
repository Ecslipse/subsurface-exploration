import argparse
import logging
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        prog="clas",
        description="Deterministic coal seam screening from LAS well-log data.",
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=35
        ),
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--las", nargs="+", metavar="FILE",help=" Path to LAS file")
    input_group.add_argument("--las-dir", metavar="DIR", help="Path to LAS directory")

    parser.add_argument("--plot", action="store_true", help="Display interactive plot")
    parser.add_argument("--save-plot", action="store_true", help="Save the plot (png) into the ouput directory")

    parser.add_argument(
        "--config",type=Path,metavar="YAML",help="Path to CLAS configuration YAML file"
    )

    parser.add_argument("--output", default="outputs", metavar="DIR",help="Path to custom output directory")
    parser.add_argument("--dry-run", action="store_true",help="Developer run")

    parser.add_argument(
        "--verbose", action="store_true", help="Verbose logging"
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress non-error output"
    )

    args = parser.parse_args()

    if args.las_dir and args.plot:
        parser.error("--plot cannot be used with --las-dir (use --save-plot)")

    return args

def setup_logging(verbose: bool, quiet: bool) -> None:
    level = logging.INFO
    if verbose:
        level = logging.DEBUG
    if quiet:
        level = logging.ERROR

    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
    )