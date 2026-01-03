import streamlit as st
import tempfile
from pathlib import Path
import pandas as pd
import sys
import time

SRC_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC_ROOT))

from core.process import process_well
from core.config import CLASConfig
from viz.plotly_qc import PlotlyQCPlot

# ------------------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------------------

st.set_page_config(page_title="C-LAS Demo", layout="wide")

st.title("C-LAS")
st.caption("Interactive QC visualization for LAS files (maximum 2 wells)")

cfg = CLASConfig()

# ------------------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------------------

defaults = {
    "processed": False,
    "results": [],}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

def reset_app():
    st.session_state.clear()
    st.rerun()

def dataframe_height_by_chunks(
    n_rows: int,
    chunk_size: int = 6,
    max_chunks: int = 3,
    row_px: int = 35,
    header_px: int = 40,
) -> int:
    chunks = ((n_rows - 1) // chunk_size + 1) if n_rows else 1
    chunks = min(chunks, max_chunks)
    return header_px + chunks * chunk_size * row_px

@st.cache_data(show_spinner=False)
def cached_process_well(las_bytes: bytes, cfg: CLASConfig) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        las_path = Path(tmpdir) / "input.las"
        las_path.write_bytes(las_bytes)
        return process_well(las_path, cfg)

# ------------------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------------------

with st.sidebar:
    st.header("Workflow")
    st.caption("Upload LAS files and run QC processing")

    uploaded_files = st.file_uploader(
        "Upload LAS file(s)",
        type=["las"],
        accept_multiple_files=True,
        disabled=st.session_state.processed,
        help="You can upload up to 2 LAS files for side-by-side comparison.",
    )
    
    use_yaml = st.sidebar.checkbox("Use custom config")
    if use_yaml:
        uploaded = st.sidebar.file_uploader(
            "Upload YAML config",
            type=["yaml", "yml"],
        )

        if uploaded:
            tmp = Path("uploaded_config.yaml")
            tmp.write_bytes(uploaded.getvalue())
            config = CLASConfig.from_yaml(tmp)
        else:
            st.stop()
    else:
        config = CLASConfig()

    if uploaded_files and len(uploaded_files) > 2:
        st.error("Maximum 2 LAS files allowed.")
        st.stop()

    if uploaded_files and not st.session_state.processed:
        st.markdown("---")
        st.caption("Start processing once all files are uploaded.")

        if st.button("Process Wells", type="primary"):
            progress = st.progress(0)
            status = st.empty()

            results = []
            total = len(uploaded_files)
            start = time.time()

            for i, f in enumerate(uploaded_files, start=1):
                status.info(f"Processing {f.name} ({i}/{total})")

                result = cached_process_well(f.read(), cfg)
                results.append(result)

                elapsed = time.time() - start
                eta = int((elapsed / i) * (total - i)) if i < total else 0

                progress.progress(i / total)
                status.caption(f"QC + Seam Extraction · ETA ~ {eta}s")

            progress.empty()
            status.success("Processing complete")

            st.session_state.results = results
            st.session_state.processed = True

# ------------------------------------------------------------------------------
# Main content
# ------------------------------------------------------------------------------

if not st.session_state.processed:
    st.info("Upload up to 2 LAS files and click **Process Wells** to begin.")
    st.stop()

results = st.session_state.results

# ------------------------------------------------------------------------------
# Adaptive layout
# ------------------------------------------------------------------------------

if len(results) == 1:
    cols = [st.container()]
else:
    cols = st.columns(2)

for idx, result in enumerate(results):
    with cols[idx]:
        st.subheader(f"Well: {result['well']}")
        st.caption("QC tracks and seam summary")

        # -------------------------------
        # Seam table
        # -------------------------------
        st.markdown("#### Seam Summary")

        seams_df = result["seams"]
        table_height = dataframe_height_by_chunks(len(seams_df))

        st.dataframe(
            seams_df,
            use_container_width=True,
            hide_index=True,
            height=table_height,
        )

        # -------------------------------
        # Plot
        # -------------------------------
        st.markdown("#### QC Tracks")

        plot = PlotlyQCPlot(
            df=result["df"],
            well_name=result["well"],
        )

        st.plotly_chart(plot.figure(), use_container_width=True)

        # -------------------------------
        # Downloads
        # -------------------------------
        st.markdown("#### Downloads")

        st.download_button(
            "Download Seam Summary (CSV)",
            data=seams_df.to_csv(index=False).encode(),
            file_name=f"{result['well']}_seams.csv",
            mime="text/csv",
        )

        st.download_button(
            "Download QC Plot (PNG)",
            data=plot.to_png(),
            file_name=f"{result['well']}_qc.png",
            mime="image/png",
        )

# ------------------------------------------------------------------------------
# Reset button
# ------------------------------------------------------------------------------

st.markdown("---")
st.caption("Reset will clear all uploaded files and results.")

if st.button("End Session (Reset)", type="primary"):
    reset_app()