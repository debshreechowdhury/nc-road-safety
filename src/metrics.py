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

import math

import pandas as pd


def serious_crash_count(df: pd.DataFrame) -> int:
    """
    Return the number of crashes classified as fatal or serious injury.

    The dataframe must contain the shared Boolean `is_serious` feature
    created by `src.preprocessing.add_shared_features()`.
    """

    return int(df["is_serious"].fillna(False).sum())


def serious_rate_per_1000(df: pd.DataFrame) -> float:
    """
    Calculate serious crashes per 1,000 recorded crashes.

    Formula
    -------
    serious crashes / all crashes * 1,000

    Returns NaN for an empty dataframe.
    """

    if len(df) == 0:
        return math.nan

    return 1000 * df["is_serious"].fillna(False).mean()


def severity_multiplier(
    group_df: pd.DataFrame,
    statewide_rate_per_1000: float,
) -> float:
    """
    Compare a subgroup's serious-outcome rate with the statewide rate.

    Formula
    -------
    subgroup serious rate / statewide serious rate

    Parameters
    ----------
    group_df : pandas.DataFrame
        Subset of crash records representing a county, crash factor,
        geographic category, or other group.

    statewide_rate_per_1000 : float
        Serious Outcome Rate for the full statewide analysis population.

    Returns
    -------
    float
        Relative serious-outcome rate.

    Examples
    --------
    1.0
        Same rate as the statewide baseline.

    2.0
        Serious outcomes occur twice as frequently among recorded
        crashes in this group as in the statewide crash population.
    """

    if (
        statewide_rate_per_1000 is None
        or pd.isna(statewide_rate_per_1000)
        or statewide_rate_per_1000 == 0
    ):
        return math.nan

    group_rate = serious_rate_per_1000(group_df)

    return group_rate / statewide_rate_per_1000