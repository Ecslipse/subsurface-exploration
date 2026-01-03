# C-LAS Roadmap

This roadmap reflects the **actual current capabilities** of C-LAS as of its first public portfolio release, and outlines realistic, incremental evolution paths.

C-LAS is positioned as a **deterministic, geology-driven screening tool** with both CLI and Streamlit interfaces. The focus is clarity, reproducibility, and professional software practices — not feature bloat.

## ✅ Current State — v1.1 (Portfolio Release)

C-LAS currently supports:

* Single LAS file processing (CLI)
* Batch directory processing (CLI)
* Dry-run / validation mode
* Deterministic, rule-based coal seam detection
* Probabilistic confidence scoring layered on deterministic logic
* Robust handling of missing data via nearest-neighbor logic
* YAML-based configuration override (optional, defaults in code)
* Matplotlib-based QC plots (`--plot`, single LAS only)
* Saved QC plots (`--save-plot`)
* Streamlit demo application with:

  * LAS upload
  * Interactive plots
  * Seam summary table (coal confidence–driven)
  * CSV + PNG export
  * Custom YAML configuration upload

* Clean modular architecture:

  * Core engine (CLI + logic)
  * Visualization layer
  * Streamlit application layer
  
* Pytest coverage for configuration, I/O, and scoring logic

This version is considered **stable and portfolio-ready**.

## 🚀 Short-Term Improvements — v1.3

### 1. CLI Export Support

**Status:** Planned

Add optional structured output export for CLI runs:

* `--export csv`
* `--export json`

Outputs:

* Seam table per well
* Summary statistics

**Rationale:** Enables downstream analysis and scripting without relying on plots alone.

---

### 2. Soft Progress Feedback for Batch Runs

**Status:** Planned

* File counter display
* Optional progress bar

Example:

```
Processing 3/12: WELL_ABC.las
```

**Rationale:** Better UX for large datasets.

## 🔧 Medium-Term Improvements — v1.4 – v1.5

### 3. Resume / Skip Processed Wells

Skip wells with existing outputs unless `--force` is specified.

**Rationale:** Faster iteration and fault tolerance.

---

### 4. Validation & Data Quality Warnings

Improve diagnostics:

* Missing GR log → error
* Missing density log → warning + fallback

**Rationale:** Transparency and user trust.

---

### 5. Sensitivity / Scenario Runs

Enable multi-parameter runs:

```bash
core --las well.las --min-thickness 0.8 1.0 1.2
```

**Rationale:** Geological interpretation and research workflows.

## 🧩 Long-Term Direction — v2.0+

### 6. Pluggable Scoring Strategies

Support multiple scoring engines:

```python
compute_clas(df, cfg, strategy="v2")
```

**Rationale:** Extendability without breaking reproducibility.

---

### 7. Advanced Streamlit UX

Potential enhancements:

* Multi-file upload
* Parameter presets
* Session-based comparison

**Rationale:** Demonstration depth and accessibility.

---

### 8. Packaging & Distribution

* Stable semantic versioning
* Formal changelog discipline
* Optional PyPI distribution

**Rationale:** Professional polish and reuse.

## 🧠 Design Principles

* CLI is the source of truth
* GUI layers reuse the same pipeline
* Deterministic core with explicit uncertainty
* Reproducible, inspectable workflows
* Minimal magic, maximum clarity

## 📌 Notes

This roadmap is intentionally conservative. Features are added only when they preserve interpretability, reproducibility, and geological reasoning.