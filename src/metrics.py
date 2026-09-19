"""
Shared road-safety metrics.

The project distinguishes crash frequency from crash severity.

Rather than creating an arbitrary weighted "danger score," the metrics
in this module are calculated directly from observed crash outcomes.

Primary metrics
---------------
Serious Outcome Rate
    Number of fatal or serious-injury crashes per 1,000 recorded crashes.

Severity Multiplier
    Serious Outcome Rate for a subgroup divided by the statewide
    Serious Outcome Rate.

A Severity Multiplier of:

    1.0 = same serious-outcome rate as the statewide baseline
    1.5 = 1.5 times the statewide serious-outcome rate
    0.7 = 70% of the statewide serious-outcome rate

These measures describe associations among recorded crashes. They should
not be interpreted as causal estimates or as complete measures of road
danger because traffic exposure is not included in the current dataset.
"""

"""Shared crash-severity metrics used across project analyses."""

import math

import pandas as pd

from src.config import KNOWN_SEVERITIES


def serious_crash_count(df):
    """
    Return the number of crashes classified as serious.

    A serious crash is defined during preprocessing as a crash with
    severity K (fatal) or A (serious/disabling injury).
    """
    return int(df["is_serious"].fillna(False).sum())


def known_severity_crash_count(df):
    """
    Return the number of crashes with a known severity.

    NCDOT severity codes K, A, B, C, and O are considered known.
    Records coded U (unknown severity) are excluded.
    """
    return int(df["CrshSeverity"].isin(KNOWN_SEVERITIES).sum())


def serious_rate_per_1000(df):
    """
    Calculate serious crashes per 1,000 crashes with known severity.

    Serious crashes are severity K or A.

    Crashes coded U (unknown severity) are excluded from the
    denominator rather than being treated as non-serious.

    Returns NaN when no crashes with known severity are available.
    """
    known_severity_mask = df["CrshSeverity"].isin(KNOWN_SEVERITIES)

    denominator = int(known_severity_mask.sum())

    if denominator == 0:
        return math.nan

    serious_count = int(
        df.loc[known_severity_mask, "is_serious"]
        .fillna(False)
        .sum()
    )

    return 1000 * serious_count / denominator


def severity_multiplier(group_df, statewide_rate_per_1000):
    """
    Compare a group's Serious Outcome Rate with the statewide rate.

    A value of:
        1.0 = same as statewide rate
        >1.0 = higher than statewide rate
        <1.0 = lower than statewide rate

    This is a descriptive comparison of recorded crash outcomes.
    It should not be interpreted as a causal measure or as a complete
    measure of roadway danger without an exposure denominator.
    """
    if (
        statewide_rate_per_1000 is None
        or pd.isna(statewide_rate_per_1000)
        or statewide_rate_per_1000 == 0
    ):
        return math.nan

    group_rate = serious_rate_per_1000(group_df)

    if pd.isna(group_rate):
        return math.nan

    return group_rate / statewide_rate_per_1000