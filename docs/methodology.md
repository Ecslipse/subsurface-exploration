# C-LAS (Coal from LAS) – Methodology

## Overview
*C-LAS* is a deterministic scoring framework designed to identify coal-bearing intervals from well-log data.

Rather than performing lithology classification, the method assigns a continuous confidence score that reflects the likelihood that a given depth interval represents coal.

The approach emphasizes geological reasoning, reproducibility, and transparency.

---

## Input Data
The method operates on standard wireline logs commonly available in coal exploration wells:

- Gamma Ray (GR)
- Bulk density (LD and/or SD)
- Caliper (CL)
- Measured depth (DEPT)

The algorithm is tolerant of missing density or caliper logs and degrades predictably when data are incomplete.

---

## Normalization
All log values are normalized using percentile-based scaling (typically 5th–95th percentiles). This approach:

- Reduces sensitivity to outliers
- Preserves relative trends
- Remains stable across different acquisition units (e.g. cps vs API)

---

## Scoring Components

### 1. Gamma Ray Suppression
Coal is typically associated with low gamma ray values. Normalized GR is inverted and scaled to emphasize low-GR intervals.

### 2. Density Reinforcement
Coal generally exhibits lower bulk density compared to surrounding sediments. When multiple density logs are available, their median is used to reduce noise.

### 3. Log Stability
Coal seams tend to display relatively stable log responses. Rolling standard deviation of the GR log is used as a proxy for lithological consistency.

### 4. Washout Penalization
Caliper logs are used to penalize intervals affected by borehole washout, which can produce false coal-like signatures.

---

## CCI Computation
Each component contributes to the final CCI score using fixed, pre-defined weights that sum to one:

CCI ∈ [0, 1]

Weights are intentionally locked to preserve deterministic behavior and geological interpretability.

---

## Seam Extraction
Continuous depth intervals exceeding a point-level CCI threshold are grouped into candidate seams. Seam-level validation applies:

- Minimum thickness
- Minimum mean CCI
- Minimum internal CCI

This two-stage validation reduces false positives caused by isolated log artifacts.

---

## Output
The final outputs include:
- Point-level CCI values
- Coal seam intervals with depth and thickness
- Quality-control plots for interpretation review

The methodology prioritizes interpretability over automation, supporting expert review rather than replacing it.