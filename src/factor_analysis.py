"""
Crash-factor and temporal analysis for the NC Road Safety project.

This module contains analysis functions for examining:

1. Annual crash trends from 2021 through 2025.
2. The frequency of selected NCDOT crash factors.
3. Serious crash outcomes associated with those factors.
4. The relationship between crash-factor frequency and severity.

Shared data loading, preprocessing, and metric definitions are located in:

    src.preprocessing
    src.metrics
    src.config

Those shared modules should not normally be modified from this feature
branch.

Analysis scope
--------------
The project defines a serious crash as an NCDOT severity K or A crash.

Serious Outcome Rate is defined as:

    K+A crashes
    --------------------------------------------- * 1,000
    crashes with known severity (K, A, B, C, O)

Records coded U (unknown severity) are retained in the source dataset
but excluded from the denominator of the Serious Outcome Rate.

Important interpretation
------------------------
Crash-factor indicators describe characteristics recorded for crashes.
They should be interpreted as associations, not necessarily as causes
of crash severity.

Individual crashes may contain multiple factor indicators. Factor
categories are therefore not mutually exclusive.
"""

import pandas as pd

from src.config import FACTOR_COLUMNS
from src.metrics import (
    known_severity_crash_count,
    serious_crash_count,
    serious_rate_per_1000,
    severity_multiplier,
)


def build_annual_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a year-level summary of crash frequency and severity.

    Expected output
    ---------------
    Return one row per year.

    At minimum, the summary should contain:

        year
        crash_count
        known_severity_count
        serious_crash_count
        serious_rate_per_1000

    Optional additions are welcome if they help the analysis.

    Notes
    -----
    The shared preprocessing pipeline already restricts the main
    analysis dataset to 2021-2025.

    TODO
    ----
    1. Group crash records by year.
    2. Calculate total crash count.
    3. Calculate crashes with known severity.
    4. Calculate K+A serious crash count.
    5. Calculate Serious Outcome Rate per 1,000 known-severity crashes.
    6. Return a tidy DataFrame sorted by year.

    Implementation is intentionally left open. You may use groupby,
    helper functions, aggregation, or another clear pandas approach.
    """

    # TODO: Implement annual crash summary.
    raise NotImplementedError


def build_factor_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize crash frequency and serious outcomes for NCDOT factors.

    Examples of factors available through FACTOR_COLUMNS include:

        Alcohol Related
        Drug Related
        Speed Related
        Distracted Driver
        Drowsy Driver
        Older Driver
        Teen Driver
        Unbelted Crash
        Motorcycle Involved
        Heavy Truck Involved
        Pedestrian Involved
        Bicycle Involved

    Expected output
    ---------------
    Return one row per factor.

    At minimum, include:

        factor
        crash_count
        known_severity_count
        serious_crash_count
        serious_rate_per_1000
        severity_multiplier

    The severity multiplier compares the factor-specific Serious
    Outcome Rate with the statewide Serious Outcome Rate.

    TODO
    ----
    For each factor in FACTOR_COLUMNS:

    1. Select crashes where that factor is recorded as True.
    2. Count the crashes involving the factor.
    3. Count crashes with known severity.
    4. Count K+A serious crashes.
    5. Calculate Serious Outcome Rate.
    6. Compare the rate with the statewide baseline using the shared
       severity_multiplier() function.
    7. Store the results in a tidy DataFrame.

    Important
    ---------
    A crash can contain multiple factors. Do not assume that factor
    counts should sum to the total number of crashes.

    Feel free to add additional useful descriptive metrics if they are
    clearly documented.
    """

    # TODO: Implement factor-level summary.
    raise NotImplementedError


def get_statewide_baseline(df: pd.DataFrame) -> float:
    """
    Return the statewide Serious Outcome Rate per 1,000 crashes with
    known severity.

    This helper can be used when calculating factor-level severity
    multipliers.
    """

    return serious_rate_per_1000(df)