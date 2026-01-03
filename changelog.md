# Changelog

All notable changes to **C-LAS (Coal Log Analysis System)** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows **Semantic Versioning**.

---

## [1.2.0] — Portfolio Release

### Added

* Streamlit demo application with:

  * LAS file upload
  * Interactive QC plots
  * Seam summary table driven by coal confidence
  * CSV and PNG export per well
  * Custom YAML configuration upload
* YAML-based configuration override system with safe defaults embedded in code
* Structured logging system with log levels (INFO, WARNING, ERROR, DEBUG)
* Verbose logging mode for detailed diagnostics
* Batch-processing guardrails preventing plotting on LAS directories
* Progress feedback for batch CLI runs (currently INFO-level logging)
* Nearest-neighbor handling for missing depth samples
* Probabilistic coal confidence scoring layered on deterministic logic
* Pytest coverage for configuration, I/O, and scoring modules

### Changed

* CLI and Streamlit now share a unified configuration loading mechanism
* Plotting behavior restricted to single-file runs to prevent infinite loops
* Internal scoring logic refactored for clarity and reproducibility

### Known Limitations

* Batch progress feedback is currently emitted via `logging.info`, which may flood terminal output
* Validation checks currently focus on depth integrity; other log curves rely on graceful degradation
* CLI does not yet support structured data export (CSV/JSON)

---

## [1.1.0] — Internal Milestone

### Added

* Deterministic, rule-based coal seam detection engine
* CLI support for single LAS file and directory processing
* Dry-run / validation mode
* Matplotlib-based QC plotting
* Saved plot export
* Modular project architecture separating core logic, visualization, and UI

---

## [1.0.0] — Initial Prototype

### Added

* Initial proof-of-concept for coal seam screening from LAS data
* Basic scoring heuristics
* Manual plotting workflow