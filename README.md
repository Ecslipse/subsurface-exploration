# 📡 C-LAS

Current version : `v1.2.0`

**C-LAS** is a Python tool for deterministic, geology-driven coal seam detection from LAS well-log data. It is designed to accelerate early-stage screening during exploration workflows,
not to replace expert geological interpretation.

## 💡 What problem does this solve?

Manual coal seam picking across large LAS datasets is slow, repetitive, and difficult to scale. C-LAS automates the *screening* stage by tagging coal-prone intervals using transparent, rule-based logic, allowing geoscientists to focus on relevant depth sections only.

## 🧠 Who is this for?

This tool is *ideal* for :

* Geophysics / geology students
* Exploration geoscientists
* Subsurface data analysts working with LAS files

## ⚙️ Skills Demonstrated

This project showcases :

- Python (packaging, CLI design)
- LAS well-log processing (`lasio`)
- Rule-based geological interpretation
- Data visualization (`matplotlib` , `plotly`)
- Web based tool integration (`streamlit`)
- Reproducible data workflows
- Git & GitHub project structuring

## 📂 Project Structure

```text
subsurface-exploration/
├── docs/          # Design notes and methodology
├── sample/        # Example LAS files
├── configs/       # Optional YAML configurations
├── src/
│   ├── core/      # Core engine + CLI
│   ├── viz/       # Plotting (matplotlib / plotly)
│   ├── app/       # Streamlit application
│   └── test/      # Pytest coverage
├── ROADMAP.md
├── CHANGELOG.md
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Option A — Streamlit Demo (recommended)

The Streamlit application provides a lightweight, interactive demonstration.

Live demo link :
`https://subsurface-exploration-clas-demo.streamlit.app/`

Features :
- Upload LAS files
- Adjust custom interpretation parameters via YAML config (optional)
- Interactive QC plots
- Seam summary table driven by confidence index
- Export results (CSV + PNG)

🔒 The hosted demo may be gated or rate-limited.

### Option B — CLI Demo (run from source)

```bash
pip git clone https://github.com/Ecslipse/subsurface-exploration.git
cd src
pip install -r requirements.txt
python -m core --las sample/example.las --plot
```

- Runs directly from repository
- Intended for evaluation and research use only

## Option C (development install)

```bash
pip git clone https://github.com/Ecslipse/subsurface-exploration.git
cd src
pip install e .
clas --las sample/example.las --plot
```

- Gives more control in CLI
- Auto install dependancies
- Intended for evaluation and research use only

## ⚙️ Configuration System

C-LAS ships with code-defined defaults to ensure zero-config usability.
Users may optionally supply a YAML file to override parameters :

```bash
python -m core --las well.las --config configs/custom.yaml
```

Only provided fields are overridden; all others fall back to defaults.

## 📘 CLI Reference

Run core `--help` for a complete list of flags and options :

```bash
python -m core --help
```

## 🎯 Example Output

![Output of the program](outputs/example1/SYNTH_A%20C-LAS%20QC.png)

## ⌛ Quick Demo

![C-LAS demo](docs/demo.gif)

## 🎓 Design Philosophy

* A rule-based approach was chosen instead of machine learning to ensure
  interpretability and geological transparency.
* All thresholds are configurable to adapt to different basin characteristics.
* The tool focuses on screening acceleration, not automated final decisions.

## 📖 Learn More

Detailed documentation is available in the `docs/` directory :

* `assumptions.md` — Data assumptions and preconditions
* `methodology.md` — Interpretation logic and design rationale
* `limitations.md` — Known limitations and use boundaries

## ⚠️ Disclaimer

C-LAS is an assistive screening tool for early-stage interpretation.
It does not replace expert geological judgment and is not intended for automated decision-making.