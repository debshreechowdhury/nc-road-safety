"""
Reusable geographic analysis functions for the NC Road Safety project.

This module contains geographic aggregation logic used by the
geography/severity analysis notebook and downstream visualizations.

The functions in this module operate on data already standardized by
src.preprocessing.
"""

import pandas as pd

from src.metrics import (
    known_severity_crash_count,
    serious_crash_count,
    serious_rate_per_1000,
    severity_multiplier,
)


def build_county_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build county-level crash frequency and severity metrics.

    Parameters
    ----------
    df : pandas.DataFrame
        Preprocessed NCDOT crash data containing County, CrshSeverity,
        and is_serious.

    Returns
    -------
    pandas.DataFrame
        One row per county containing:

        - County
        - crash_count
        - known_severity_count
        - serious_crash_count
        - serious_rate_per_1000
        - severity_multiplier

    Notes
    -----
    Serious Outcome Rate represents K+A crashes per 1,000 recorded
    crashes with known severity.

    Severity multiplier compares each county's Serious Outcome Rate
    with the statewide Serious Outcome Rate.

    These metrics describe outcomes among recorded crashes. They are
    not exposure-adjusted measures of roadway crash risk.
    """
    statewide_rate = serious_rate_per_1000(df)

    records = []

    for county, county_df in df.groupby("County"):
        records.append({
            "County": county,
            "crash_count": len(county_df),
            "known_severity_count": known_severity_crash_count(county_df),
            "serious_crash_count": serious_crash_count(county_df),
            "serious_rate_per_1000": serious_rate_per_1000(county_df),
            "severity_multiplier": severity_multiplier(
                county_df,
                statewide_rate,
            ),
        })

    return (
        pd.DataFrame(records)
        .sort_values("crash_count", ascending=False)
        .reset_index(drop=True)
    )