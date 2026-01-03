import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class PlotlyQCPlot:

    def __init__(
        self,
        df: pd.DataFrame,
        well_name: str,
        threshold: float = 0.7,
    ):
        self.df = df
        self.well = well_name
        self.threshold = threshold
        self.fig = self._build()

    # --------------------------------------------------
    # Build figure
    # --------------------------------------------------
    def _build(self) -> go.Figure:
        fig = make_subplots(
            rows=1,
            cols=3,
            shared_yaxes=True,
            horizontal_spacing=0.05,
            column_widths=[0.33, 0.33, 0.34],
            subplot_titles=("Gamma Ray", "Density", "CCI"),
        )

        self._gr_track(fig, col=1)
        self._density_track(fig, col=2)
        self._cci_track(fig, col=3)

        fig.update_yaxes(
            autorange="reversed",
            title_text="",
            showgrid=True,
        )

        fig.update_layout(
            height=800,
            template="simple_white",
            showlegend=False,
            margin=dict(l=60, r=40, t=80, b=40),
        )

        return fig

    # --------------------------------------------------
    # GR track, Density track
    # --------------------------------------------------
    def _gr_track(self, fig: go.Figure, col: int) -> None:
        if "GR" not in self.df:
            return

        fig.add_trace(
            go.Scatter(
                x=self.df["GR"],
                y=self.df["DEPT"],
                mode="lines",
                line=dict(color="darkgreen"),
            ),
            row=1,
            col=col,
        )

        fig.update_xaxes(title_text="GR", row=1, col=col)

    def _density_track(self, fig: go.Figure, col: int) -> None:
        dens_cols = [c for c in ("LD", "SD") if c in self.df.columns]
        if not dens_cols:
            return

        dens = self.df[dens_cols].median(axis=1, skipna=True)

        fig.add_trace(
            go.Scatter(
                x=dens,
                y=self.df["DEPT"],
                mode="lines",
                line=dict(color="navy"),
            ),
            row=1,
            col=col,
        )

        fig.update_xaxes(title_text="Density", row=1, col=col)

    def _cci_track(self, fig: go.Figure, col: int) -> None:
        if "CLAS" not in self.df:
            return

        # -----------------------------
        # CLAS scatter plot
        # -----------------------------
        mask_pos = self.df["CLAS"].notna() & (self.df["CLAS"] > 0)

        fig.add_trace(
            go.Scatter(
                x=self.df.loc[mask_pos, "CLAS"],
                y=self.df.loc[mask_pos, "DEPT"],
                mode="markers",
                marker=dict(
                    size=6,
                    color=self.df.loc[mask_pos, "CLAS"],
                    colorscale="Viridis",
                    cmin=0,
                    cmax=1,
                    colorbar=dict(title="CCI"),
                ),
            ),
            row=1,
            col=col,
        )

        fig.update_xaxes(
            title_text="CCI",
            range=[0, 1],
            row=1,
            col=col,
        )

    # --------------------------------------------------
    # Applying save function
    # --------------------------------------------------
    def figure(self) -> go.Figure:
        return self.fig

    def to_png(
        self,
        width: int = 1400,
        height: int = 800,
        scale: int = 2,
    ) -> bytes:
        return self.fig.to_image(
            format="png",
            width=width,
            height=height,
            scale=scale,
        )