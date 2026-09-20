"""
Visualization functions for crash-factor and temporal analysis.

This module is responsible for presentation-ready visualizations built
from the summary tables created in src.factor_analysis.

The analysis calculations should remain in factor_analysis.py whenever
possible. This file should focus primarily on visualization.

Suggested outputs
-----------------
1. Annual crash/severity trend.
2. Crash-factor frequency comparison.
3. Frequency-versus-severity visualization.

The exact chart design is intentionally flexible. Alternative
visualizations are welcome if they communicate the same analytical
question more effectively.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_annual_trend(
    annual_summary: pd.DataFrame,
    output_path: Path | None = None,
):
    """
    Visualize crash trends from 2021-2025.

    Suggested question
    ------------------
    How have recorded crash frequency and serious crash outcomes changed
    over the five complete analysis years?

    TODO
    ----
    Create a clear visualization using annual_summary.

    Possible approaches include:
        - total crashes by year;
        - serious crashes by year;
        - Serious Outcome Rate by year;
        - or a combination that remains easy to interpret.

    Avoid misleading dual-axis charts unless there is a strong reason
    to use one.

    If output_path is provided, save the figure there.

    Return the matplotlib figure/axes so the visualization can also be
    used interactively.
    """

    # TODO: Implement visualization.
    raise NotImplementedError


def plot_factor_frequency_vs_severity(
    factor_summary: pd.DataFrame,
    output_path: Path | None = None,
):
    """
    Compare how frequently crash factors occur with their serious
    outcome rates.

    Core storytelling question
    --------------------------
    Are the factors that occur most frequently also the factors with
    the highest Serious Outcome Rate?

    Suggested approach
    ------------------
    A scatter plot can work well:

        x-axis = number of crashes involving the factor
        y-axis = Serious Outcome Rate or severity multiplier

    Each point can represent one crash factor.

    This is only a suggestion. Another visualization is acceptable if
    it communicates the frequency-versus-severity distinction clearly.

    TODO
    ----
    1. Create the visualization.
    2. Clearly label the metric and units.
    3. Make factor names understandable to a general audience.
    4. Consider labeling notable points without overcrowding the chart.
    5. Save the figure when output_path is provided.
    6. Return the figure/axes.

    Interpretation caution
    ----------------------
    The visualization shows descriptive associations in recorded crash
    data. It should not imply that a factor causes serious outcomes.
    """

    # TODO: Implement visualization.
    raise NotImplementedError